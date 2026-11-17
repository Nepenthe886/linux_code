"""Mecanum-wheel kinematics and keyboard mapping for the Zhirong Cup robot.

The robot "麦伦" uses four mecanum wheels in an X layout.  The geometry below
matches ``src/robot/robot_description/urdf/omni_robot.urdf`` exactly:

* wheel radius            ``r  = 0.065 m``
* wheel centre offset X   ``bx = 0.170 m``  (wheel axis plane, front/rear)
* wheel centre offset Y   ``by = 0.170 m``  (wheel axis plane, left/right)

Every wheel joint uses ``axis="0 1 0"`` (``+Y``), so a *positive* joint
velocity rolls every wheel towards the robot front (``+X``).  Keep that
convention when you connect a real motor driver: positive wheel speed must
make the robot drive forward with all four wheels.

Wheel order is always ``FL, FR, RL, RR``:
``wheel_front_left_joint``, ``wheel_front_right_joint``,
``wheel_rear_left_joint``, ``wheel_rear_right_joint``.

Inverse kinematics (body velocity -> wheel angular velocity)::

    w_FL = ( vx - vy - (bx + by) * wz ) / r
    w_FR = ( vx + vy + (bx + by) * wz ) / r
    w_RL = ( vx + vy - (bx + by) * wz ) / r
    w_RR = ( vx - vy + (bx + by) * wz ) / r

Forward kinematics (wheel angular velocity -> body velocity)::

    vx = r/4              * ( w_FL + w_FR + w_RL + w_RR )
    vy = r/4              * (-w_FL + w_FR + w_RL - w_RR )
    wz = r / (4 (bx+by))  * (-w_FL + w_FR - w_RL + w_RR )

The sign convention may need a per-wheel ``+/-1`` calibration mask on the real
robot (roller direction, motor mounting); the ``wheel_signs`` argument of
:class:`MecanumKinematics` exists for exactly that purpose and defaults to all
``+1``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

__all__ = [
    "WHEEL_NAMES",
    "WHEEL_LABELS",
    "WHEEL_JOINTS",
    "BodyVelocity",
    "MecanumKinematics",
    "KEY_ALIASES",
    "ACTION_LABELS",
    "ACTION_KEY_HINTS",
    "CANONICAL_ACTIONS",
    "key_action",
    "keys_to_actions",
    "keys_to_body",
    "wheel_rps",
    "format_wheels",
]

#: Joint names of the four wheels, robot wheel order FL, FR, RL, RR.
WHEEL_NAMES: tuple[str, str, str, str] = (
    "wheel_front_left_joint",
    "wheel_front_right_joint",
    "wheel_rear_left_joint",
    "wheel_rear_right_joint",
)
#: Short labels used by logging / the GUI.
WHEEL_LABELS: tuple[str, str, str, str] = ("FL", "FR", "RL", "RR")
#: Alias kept for readability in loops that talk about joints.
WHEEL_JOINTS = WHEEL_NAMES

#: Canonical motion actions produced by the keyboard layer.
CANONICAL_ACTIONS = frozenset(
    {
        "forward",
        "backward",
        "left",
        "right",
        "rotate_left",
        "rotate_right",
        "stop",
    }
)

#: Human readable action names (Chinese UI labels).
ACTION_LABELS: Mapping[str, str] = {
    "forward": "前进",
    "backward": "后退",
    "left": "左平移",
    "right": "右平移",
    "rotate_left": "左转",
    "rotate_right": "右转",
    "stop": "停止",
}

#: Primary key hint per action, shown in the GUI legend / terminal help.
ACTION_KEY_HINTS: Mapping[str, str] = {
    "forward": "W / ↑",
    "backward": "S / ↓",
    "left": "A / ←",
    "right": "D / →",
    "rotate_left": "Q",
    "rotate_right": "E",
    "stop": "空格",
}

#: Raw key symbol -> canonical action.
#:
#: The table accepts ``str`` characters (``w``/``W``), Tkinter keysyms
#: (``Up``, ``Left``, ...) and curses key names (``KEY_UP``, ...).  Unknown
#: keys return ``None`` from :func:`key_action` and are simply ignored.
KEY_ALIASES: Mapping[str, str] = {
    # WASD (both cases, for Caps Lock / Shift users)
    "w": "forward",
    "W": "forward",
    "s": "backward",
    "S": "backward",
    "a": "left",
    "A": "left",
    "d": "right",
    "D": "right",
    # rotation in place (bonus keys, useful for tuning)
    "q": "rotate_left",
    "Q": "rotate_left",
    "e": "rotate_right",
    "E": "rotate_right",
    # arrow keys: Tkinter / X11 keysyms
    "Up": "forward",
    "Down": "backward",
    "Left": "left",
    "Right": "right",
    # arrow keys: curses / raw terminal key names
    "KEY_UP": "forward",
    "KEY_DOWN": "backward",
    "KEY_LEFT": "left",
    "KEY_RIGHT": "right",
    # emergency stop
    " ": "stop",
    "space": "stop",
    "KEY_SPACE": "stop",
}


def key_action(key: str) -> str | None:
    """Map a raw key symbol to a canonical motion action.

    Returns ``None`` for keys that are not part of the motion key map.
    """
    if not isinstance(key, str) or not key:
        return None
    if key in KEY_ALIASES:
        return KEY_ALIASES[key]
    # single character fallback (e.g. uppercase handled, keysym cases)
    lowered = key.lower()
    return KEY_ALIASES.get(lowered)


def keys_to_actions(keys: Iterable[str]) -> set[str]:
    """Normalize an iterable of raw keys into a set of canonical actions."""
    actions: set[str] = set()
    for key in keys:
        action = key_action(key)
        if action is not None:
            actions.add(action)
    return actions


@dataclass(frozen=True)
class BodyVelocity:
    """Twist of the robot body in its own frame: ``vx`` forward, ``vy`` left."""

    vx: float = 0.0
    vy: float = 0.0
    wz: float = 0.0

    def is_zero(self, eps: float = 1e-9) -> bool:
        return abs(self.vx) <= eps and abs(self.vy) <= eps and abs(self.wz) <= eps

    def speed(self) -> float:
        """Planar speed magnitude (m/s), ignoring rotation."""
        return math.hypot(self.vx, self.vy)

    def scaled(self, factor: float) -> "BodyVelocity":
        return BodyVelocity(self.vx * factor, self.vy * factor, self.wz * factor)


def keys_to_body(
    keys: Iterable[str],
    max_linear: float = 0.30,
    max_lateral: float = 0.30,
    max_angular: float = 1.00,
) -> BodyVelocity:
    """Convert the currently pressed keys into a body velocity command.

    ``w``/``Up`` -> ``+vx`` forward, ``s``/``Down`` -> ``-vx``,
    ``a``/``Left`` -> ``+vy`` (left strafe), ``d``/``Right`` -> ``-vy``
    (right strafe), ``q``/``e`` -> ``+/-wz``; ``space`` forces a stop.

    Diagonal key combinations are scaled so that the resulting planar speed
    never exceeds ``max(max_linear, max_lateral)``.
    """
    actions = keys_to_actions(keys)
    if "stop" in actions:
        return BodyVelocity()

    vx = float("forward" in actions) - float("backward" in actions)
    vy = float("left" in actions) - float("right" in actions)
    wz = float("rotate_left" in actions) - float("rotate_right" in actions)

    vx *= max_linear
    vy *= max_lateral

    linear_cap = max(abs(max_linear), abs(max_lateral))
    norm = math.hypot(vx, vy)
    if linear_cap > 0.0 and norm > linear_cap:
        scale = linear_cap / norm
        vx *= scale
        vy *= scale

    wz *= max_angular
    return BodyVelocity(vx, vy, wz)


def wheel_rps(wheel_rad_s: float) -> float:
    """Convert a wheel angular velocity [rad/s] to revolutions per second."""
    return wheel_rad_s / (2.0 * math.pi)


def format_wheels(wheels: Sequence[float]) -> str:
    """Format four wheel speeds for a one-line log/UI string."""
    return "  ".join(
        f"{label}={value:+.2f}"
        for label, value in zip(WHEEL_LABELS, wheels)
    )


class MecanumKinematics:
    """Inverse / forward kinematics of the four mecanum wheels.

    Parameters
    ----------
    wheel_radius:
        Wheel radius ``r`` [m].
    wheel_base_x, wheel_base_y:
        Distance from the body centre to the wheel *axis plane* along X and Y
        [m].  The rotation lever arm is ``wheel_base_x + wheel_base_y``.
    max_wheel_speed:
        Absolute wheel speed limit [rad/s] used by :meth:`body_to_limited_wheels`.
    wheel_signs:
        Optional per-wheel calibration mask, applied *after* the ideal
        kinematics.  ``(+1, +1, +1, +1)`` (default) matches the URDF.
    """

    def __init__(
        self,
        wheel_radius: float = 0.065,
        wheel_base_x: float = 0.170,
        wheel_base_y: float = 0.170,
        max_wheel_speed: float = 30.0,
        wheel_signs: Sequence[float] = (1.0, 1.0, 1.0, 1.0),
    ) -> None:
        if wheel_radius <= 0.0:
            raise ValueError("wheel_radius must be positive")
        if wheel_base_x <= 0.0 or wheel_base_y <= 0.0:
            raise ValueError("wheel_base_x / wheel_base_y must be positive")
        if len(tuple(wheel_signs)) != 4:
            raise ValueError("wheel_signs must contain four values")

        self.wheel_radius = float(wheel_radius)
        self.wheel_base_x = float(wheel_base_x)
        self.wheel_base_y = float(wheel_base_y)
        self.max_wheel_speed = float(max_wheel_speed)
        self.wheel_signs: tuple[float, float, float, float] = tuple(  # type: ignore[assignment]
            float(sign) for sign in wheel_signs
        )

    @property
    def lever_arm(self) -> float:
        """Rotation lever arm ``bx + by`` used by the inverse kinematics."""
        return self.wheel_base_x + self.wheel_base_y

    # ------------------------------------------------------------------ #
    # kinematics
    # ------------------------------------------------------------------ #
    def body_to_ideal_wheels(self, vx: float, vy: float, wz: float) -> tuple[float, float, float, float]:
        """Ideal (uncalibrated) wheel angular velocities for a body velocity."""
        r = self.wheel_radius
        arm = self.lever_arm * wz
        return (
            (vx - vy - arm) / r,
            (vx + vy + arm) / r,
            (vx + vy - arm) / r,
            (vx - vy + arm) / r,
        )

    def body_to_wheels(self, vx: float, vy: float, wz: float) -> tuple[float, float, float, float]:
        """Wheel angular velocities [rad/s] for a body twist, with wheel signs."""
        ideal = self.body_to_ideal_wheels(vx, vy, wz)
        return tuple(  # type: ignore[return-value]
            value * sign for value, sign in zip(ideal, self.wheel_signs)
        )

    def wheels_to_body(self, wheels: Sequence[float]) -> BodyVelocity:
        """Body velocity from wheel angular velocities (inverse of above)."""
        if len(wheels) != 4:
            raise ValueError("wheels must contain four values")
        # Undo the calibration mask before the ideal forward kinematics.
        w_fl, w_fr, w_rl, w_rr = (
            float(value) * sign
            for value, sign in zip(wheels, self.wheel_signs)
        )
        r = self.wheel_radius
        arm = 4.0 * self.lever_arm
        return BodyVelocity(
            vx=r / 4.0 * (w_fl + w_fr + w_rl + w_rr),
            vy=r / 4.0 * (-w_fl + w_fr + w_rl - w_rr),
            wz=r / arm * (-w_fl + w_fr - w_rl + w_rr),
        )

    # ------------------------------------------------------------------ #
    # limits
    # ------------------------------------------------------------------ #
    def clamp_wheels(
        self,
        wheels: Sequence[float],
        max_wheel_speed: float | None = None,
    ) -> tuple[float, float, float, float]:
        """Scale all four wheel speeds uniformly to respect the speed limit.

        Uniform scaling keeps the commanded direction of travel intact (unlike
        clipping each wheel separately, which would bend the trajectory).
        """
        limit = self.max_wheel_speed if max_wheel_speed is None else float(max_wheel_speed)
        values = [float(value) for value in wheels]
        if len(values) != 4:
            raise ValueError("wheels must contain four values")
        if limit <= 0.0:
            return (0.0, 0.0, 0.0, 0.0)
        peak = max(abs(value) for value in values)
        if peak > limit:
            scale = limit / peak
            values = [value * scale for value in values]
        return tuple(values)  # type: ignore[return-value]

    def body_to_limited_wheels(
        self,
        vx: float,
        vy: float,
        wz: float,
        max_wheel_speed: float | None = None,
    ) -> tuple[float, float, float, float]:
        """Wheel command for a body velocity, uniformly limited in speed."""
        return self.clamp_wheels(
            self.body_to_wheels(vx, vy, wz), max_wheel_speed=max_wheel_speed
        )

    def body_to_limited_velocity(
        self,
        vx: float,
        vy: float,
        wz: float,
        max_wheel_speed: float | None = None,
    ) -> tuple[BodyVelocity, tuple[float, float, float, float]]:
        """Return the feasible body velocity *and* the matching wheel command.

        Useful for the GUI: show the velocity that is actually applied after
        the wheel speed limit, and the four wheel targets in one call.
        """
        wheels = self.body_to_wheels(vx, vy, wz)
        limited = self.clamp_wheels(wheels, max_wheel_speed=max_wheel_speed)
        return self.wheels_to_body(limited), limited
