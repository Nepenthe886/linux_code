#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to gazebo_msgs__msg__ContactState

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ContactState {
    /// text info on this contact
    pub info: std::string::String,

    /// name of contact collision1
    pub collision1_name: std::string::String,

    /// name of contact collision2
    pub collision2_name: std::string::String,

    /// list of forces/torques
    pub wrenches: Vec<geometry_msgs::msg::Wrench>,

    /// sum of forces/torques in every DOF
    pub total_wrench: geometry_msgs::msg::Wrench,

    /// list of contact position
    pub contact_positions: Vec<geometry_msgs::msg::Vector3>,

    /// list of contact normals
    pub contact_normals: Vec<geometry_msgs::msg::Vector3>,

    /// list of penetration depths
    pub depths: Vec<f64>,

}



impl Default for ContactState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ContactState::default())
  }
}

impl rosidl_runtime_rs::Message for ContactState {
  type RmwMsg = super::msg::rmw::ContactState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: msg.info.as_str().into(),
        collision1_name: msg.collision1_name.as_str().into(),
        collision2_name: msg.collision2_name.as_str().into(),
        wrenches: msg.wrenches
          .into_iter()
          .map(|elem| geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        total_wrench: geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Owned(msg.total_wrench)).into_owned(),
        contact_positions: msg.contact_positions
          .into_iter()
          .map(|elem| geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        contact_normals: msg.contact_normals
          .into_iter()
          .map(|elem| geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        depths: msg.depths.as_slice().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: msg.info.as_str().into(),
        collision1_name: msg.collision1_name.as_str().into(),
        collision2_name: msg.collision2_name.as_str().into(),
        wrenches: msg.wrenches
          .iter()
          .map(|elem| geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        total_wrench: geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Borrowed(&msg.total_wrench)).into_owned(),
        contact_positions: msg.contact_positions
          .iter()
          .map(|elem| geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        contact_normals: msg.contact_normals
          .iter()
          .map(|elem| geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        depths: msg.depths.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      info: msg.info.to_string(),
      collision1_name: msg.collision1_name.to_string(),
      collision2_name: msg.collision2_name.to_string(),
      wrenches: msg.wrenches
          .into_iter()
          .map(geometry_msgs::msg::Wrench::from_rmw_message)
          .collect(),
      total_wrench: geometry_msgs::msg::Wrench::from_rmw_message(msg.total_wrench),
      contact_positions: msg.contact_positions
          .into_iter()
          .map(geometry_msgs::msg::Vector3::from_rmw_message)
          .collect(),
      contact_normals: msg.contact_normals
          .into_iter()
          .map(geometry_msgs::msg::Vector3::from_rmw_message)
          .collect(),
      depths: msg.depths.into(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__ContactsState

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ContactsState {
    /// stamp
    pub header: std_msgs::msg::Header,

    /// array of geom pairs in contact
    pub states: Vec<super::msg::ContactState>,

}



impl Default for ContactsState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ContactsState::default())
  }
}

impl rosidl_runtime_rs::Message for ContactsState {
  type RmwMsg = super::msg::rmw::ContactsState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        states: msg.states
          .into_iter()
          .map(|elem| super::msg::ContactState::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        states: msg.states
          .iter()
          .map(|elem| super::msg::ContactState::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      states: msg.states
          .into_iter()
          .map(super::msg::ContactState::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__EntityState
/// Holds an entity's pose and twist

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EntityState {
    /// Entity's scoped name.
    /// An entity can be a model, link, collision, light, etc.
    /// Be sure to use gazebo scoped naming notation (e.g.)
    pub name: std::string::String,

    /// Pose in reference frame.
    pub pose: geometry_msgs::msg::Pose,

    /// Twist in reference frame.
    pub twist: geometry_msgs::msg::Twist,

    /// Pose/twist are expressed relative to the frame of this entity.
    /// Leaving empty or "world" defaults to inertial world frame.
    pub reference_frame: std::string::String,

}



impl Default for EntityState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::EntityState::default())
  }
}

impl rosidl_runtime_rs::Message for EntityState {
  type RmwMsg = super::msg::rmw::EntityState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Owned(msg.twist)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Borrowed(&msg.twist)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      twist: geometry_msgs::msg::Twist::from_rmw_message(msg.twist),
      reference_frame: msg.reference_frame.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__LinkState
/// Deprecated, kept for ROS 1 bridge.
/// Use EntityState
/// @todo: FIXME: sets pose and twist of a link.  All children link poses/twists of the URDF tree are not updated accordingly, but should be.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LinkState {
    /// link name, link_names are in gazebo scoped name notation,
    pub link_name: std::string::String,

    /// desired pose in reference frame
    pub pose: geometry_msgs::msg::Pose,

    /// desired twist in reference frame
    pub twist: geometry_msgs::msg::Twist,

    /// set pose/twist relative to the frame of this link/body
    /// leave empty or "world" or "map" defaults to world-frame
    pub reference_frame: std::string::String,

}



impl Default for LinkState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::LinkState::default())
  }
}

impl rosidl_runtime_rs::Message for LinkState {
  type RmwMsg = super::msg::rmw::LinkState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Owned(msg.twist)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Borrowed(&msg.twist)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      link_name: msg.link_name.to_string(),
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      twist: geometry_msgs::msg::Twist::from_rmw_message(msg.twist),
      reference_frame: msg.reference_frame.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__LinkStates
/// broadcast all link states in world frame

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LinkStates {
    /// link names
    pub name: Vec<std::string::String>,

    /// desired pose in world frame
    pub pose: Vec<geometry_msgs::msg::Pose>,

    /// desired twist in world frame
    pub twist: Vec<geometry_msgs::msg::Twist>,

}



impl Default for LinkStates {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::LinkStates::default())
  }
}

impl rosidl_runtime_rs::Message for LinkStates {
  type RmwMsg = super::msg::rmw::LinkStates;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        pose: msg.pose
          .into_iter()
          .map(|elem| geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        twist: msg.twist
          .into_iter()
          .map(|elem| geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        pose: msg.pose
          .iter()
          .map(|elem| geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        twist: msg.twist
          .iter()
          .map(|elem| geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      pose: msg.pose
          .into_iter()
          .map(geometry_msgs::msg::Pose::from_rmw_message)
          .collect(),
      twist: msg.twist
          .into_iter()
          .map(geometry_msgs::msg::Twist::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__ModelState
/// Deprecated, kept for ROS 1 bridge.
/// Use EntityState
/// Set Gazebo Model pose and twist

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ModelState {
    /// model to set state (pose and twist)
    pub model_name: std::string::String,

    /// desired pose in reference frame
    pub pose: geometry_msgs::msg::Pose,

    /// desired twist in reference frame
    pub twist: geometry_msgs::msg::Twist,

    /// set pose/twist relative to the frame of this entity (Body/Model)
    /// leave empty or "world" or "map" defaults to world-frame
    pub reference_frame: std::string::String,

}



impl Default for ModelState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ModelState::default())
  }
}

impl rosidl_runtime_rs::Message for ModelState {
  type RmwMsg = super::msg::rmw::ModelState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Owned(msg.twist)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Borrowed(&msg.twist)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model_name: msg.model_name.to_string(),
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      twist: geometry_msgs::msg::Twist::from_rmw_message(msg.twist),
      reference_frame: msg.reference_frame.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__ModelStates
/// broadcast all model states in world frame

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ModelStates {
    /// model names
    pub name: Vec<std::string::String>,

    /// desired pose in world frame
    pub pose: Vec<geometry_msgs::msg::Pose>,

    /// desired twist in world frame
    pub twist: Vec<geometry_msgs::msg::Twist>,

}



impl Default for ModelStates {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ModelStates::default())
  }
}

impl rosidl_runtime_rs::Message for ModelStates {
  type RmwMsg = super::msg::rmw::ModelStates;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        pose: msg.pose
          .into_iter()
          .map(|elem| geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        twist: msg.twist
          .into_iter()
          .map(|elem| geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        pose: msg.pose
          .iter()
          .map(|elem| geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        twist: msg.twist
          .iter()
          .map(|elem| geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      pose: msg.pose
          .into_iter()
          .map(geometry_msgs::msg::Pose::from_rmw_message)
          .collect(),
      twist: msg.twist
          .into_iter()
          .map(geometry_msgs::msg::Twist::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__ODEJointProperties
/// access to low level joint properties, change these at your own risk

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ODEJointProperties {
    /// joint damping
    pub damping: Vec<f64>,

    /// joint limit
    pub hi_stop: Vec<f64>,

    /// joint limit
    pub lo_stop: Vec<f64>,

    /// set joint erp
    pub erp: Vec<f64>,

    /// set joint cfm
    pub cfm: Vec<f64>,

    /// set joint erp for joint limit "contact" joint
    pub stop_erp: Vec<f64>,

    /// set joint cfm for joint limit "contact" joint
    pub stop_cfm: Vec<f64>,

    /// joint fudge_factor applied at limits, see ODE manual for info.
    pub fudge_factor: Vec<f64>,

    /// ode joint param fmax
    pub fmax: Vec<f64>,

    /// ode joint param vel
    pub vel: Vec<f64>,

}



impl Default for ODEJointProperties {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ODEJointProperties::default())
  }
}

impl rosidl_runtime_rs::Message for ODEJointProperties {
  type RmwMsg = super::msg::rmw::ODEJointProperties;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        damping: msg.damping.as_slice().into(),
        hi_stop: msg.hi_stop.as_slice().into(),
        lo_stop: msg.lo_stop.as_slice().into(),
        erp: msg.erp.as_slice().into(),
        cfm: msg.cfm.as_slice().into(),
        stop_erp: msg.stop_erp.as_slice().into(),
        stop_cfm: msg.stop_cfm.as_slice().into(),
        fudge_factor: msg.fudge_factor.as_slice().into(),
        fmax: msg.fmax.as_slice().into(),
        vel: msg.vel.as_slice().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        damping: msg.damping.as_slice().into(),
        hi_stop: msg.hi_stop.as_slice().into(),
        lo_stop: msg.lo_stop.as_slice().into(),
        erp: msg.erp.as_slice().into(),
        cfm: msg.cfm.as_slice().into(),
        stop_erp: msg.stop_erp.as_slice().into(),
        stop_cfm: msg.stop_cfm.as_slice().into(),
        fudge_factor: msg.fudge_factor.as_slice().into(),
        fmax: msg.fmax.as_slice().into(),
        vel: msg.vel.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      damping: msg.damping.into(),
      hi_stop: msg.hi_stop.into(),
      lo_stop: msg.lo_stop.into(),
      erp: msg.erp.into(),
      cfm: msg.cfm.into(),
      stop_erp: msg.stop_erp.into(),
      stop_cfm: msg.stop_cfm.into(),
      fudge_factor: msg.fudge_factor.into(),
      fmax: msg.fmax.into(),
      vel: msg.vel.into(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__ODEPhysics

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ODEPhysics {
    /// enable auto disabling of bodies, default false
    pub auto_disable_bodies: bool,

    /// preconditioning inner iterations when uisng projected Gauss Seidel
    pub sor_pgs_precon_iters: u32,

    /// inner iterations when uisng projected Gauss Seidel
    pub sor_pgs_iters: u32,

    /// relaxation parameter when using projected Gauss Seidel, 1 = no relaxation
    pub sor_pgs_w: f64,

    /// rms error tolerance before stopping inner iterations
    pub sor_pgs_rms_error_tol: f64,

    /// contact "dead-band" width
    pub contact_surface_layer: f64,

    /// contact maximum correction velocity
    pub contact_max_correcting_vel: f64,

    /// global constraint force mixing
    pub cfm: f64,

    /// global error reduction parameter
    pub erp: f64,

    /// maximum contact joints between two geoms
    pub max_contacts: u32,

}



impl Default for ODEPhysics {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ODEPhysics::default())
  }
}

impl rosidl_runtime_rs::Message for ODEPhysics {
  type RmwMsg = super::msg::rmw::ODEPhysics;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        auto_disable_bodies: msg.auto_disable_bodies,
        sor_pgs_precon_iters: msg.sor_pgs_precon_iters,
        sor_pgs_iters: msg.sor_pgs_iters,
        sor_pgs_w: msg.sor_pgs_w,
        sor_pgs_rms_error_tol: msg.sor_pgs_rms_error_tol,
        contact_surface_layer: msg.contact_surface_layer,
        contact_max_correcting_vel: msg.contact_max_correcting_vel,
        cfm: msg.cfm,
        erp: msg.erp,
        max_contacts: msg.max_contacts,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      auto_disable_bodies: msg.auto_disable_bodies,
      sor_pgs_precon_iters: msg.sor_pgs_precon_iters,
      sor_pgs_iters: msg.sor_pgs_iters,
      sor_pgs_w: msg.sor_pgs_w,
      sor_pgs_rms_error_tol: msg.sor_pgs_rms_error_tol,
      contact_surface_layer: msg.contact_surface_layer,
      contact_max_correcting_vel: msg.contact_max_correcting_vel,
      cfm: msg.cfm,
      erp: msg.erp,
      max_contacts: msg.max_contacts,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      auto_disable_bodies: msg.auto_disable_bodies,
      sor_pgs_precon_iters: msg.sor_pgs_precon_iters,
      sor_pgs_iters: msg.sor_pgs_iters,
      sor_pgs_w: msg.sor_pgs_w,
      sor_pgs_rms_error_tol: msg.sor_pgs_rms_error_tol,
      contact_surface_layer: msg.contact_surface_layer,
      contact_max_correcting_vel: msg.contact_max_correcting_vel,
      cfm: msg.cfm,
      erp: msg.erp,
      max_contacts: msg.max_contacts,
    }
  }
}


// Corresponds to gazebo_msgs__msg__PerformanceMetrics

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PerformanceMetrics {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub real_time_factor: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sensors: Vec<super::msg::SensorPerformanceMetric>,

}



impl Default for PerformanceMetrics {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::PerformanceMetrics::default())
  }
}

impl rosidl_runtime_rs::Message for PerformanceMetrics {
  type RmwMsg = super::msg::rmw::PerformanceMetrics;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        real_time_factor: msg.real_time_factor,
        sensors: msg.sensors
          .into_iter()
          .map(|elem| super::msg::SensorPerformanceMetric::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      real_time_factor: msg.real_time_factor,
        sensors: msg.sensors
          .iter()
          .map(|elem| super::msg::SensorPerformanceMetric::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      real_time_factor: msg.real_time_factor,
      sensors: msg.sensors
          .into_iter()
          .map(super::msg::SensorPerformanceMetric::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__SensorPerformanceMetric

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SensorPerformanceMetric {

    // This member is not documented.
    #[allow(missing_docs)]
    pub name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sim_update_rate: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub real_update_rate: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fps: f64,

}



impl Default for SensorPerformanceMetric {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SensorPerformanceMetric::default())
  }
}

impl rosidl_runtime_rs::Message for SensorPerformanceMetric {
  type RmwMsg = super::msg::rmw::SensorPerformanceMetric;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        sim_update_rate: msg.sim_update_rate,
        real_update_rate: msg.real_update_rate,
        fps: msg.fps,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      sim_update_rate: msg.sim_update_rate,
      real_update_rate: msg.real_update_rate,
      fps: msg.fps,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      sim_update_rate: msg.sim_update_rate,
      real_update_rate: msg.real_update_rate,
      fps: msg.fps,
    }
  }
}


// Corresponds to gazebo_msgs__msg__WheelSlip
/// This is a message that holds data to describe the wheel slip for a set of wheels.
///
/// The wheel slip is defined by
///  * the lateral slip of the wheel, as an angle from the direction of travel (radians), and
///  * the longitudinal slip of the wheel, as a percentage of the current wheel's speed
///
/// Each wheel is uniquely identified by its name.
///
/// This message consists of multiple arrays.
/// All arrays in this message should be the same size.
/// This is the only way to uniquely associate the wheel name with the correct slip values.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WheelSlip {

    // This member is not documented.
    #[allow(missing_docs)]
    pub name: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lateral_slip: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub longitudinal_slip: Vec<f64>,

}



impl Default for WheelSlip {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::WheelSlip::default())
  }
}

impl rosidl_runtime_rs::Message for WheelSlip {
  type RmwMsg = super::msg::rmw::WheelSlip;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        lateral_slip: msg.lateral_slip.as_slice().into(),
        longitudinal_slip: msg.longitudinal_slip.as_slice().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        lateral_slip: msg.lateral_slip.as_slice().into(),
        longitudinal_slip: msg.longitudinal_slip.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      lateral_slip: msg.lateral_slip.into(),
      longitudinal_slip: msg.longitudinal_slip.into(),
    }
  }
}


// Corresponds to gazebo_msgs__msg__WorldState
/// This is a message that holds data necessary to reconstruct a snapshot of the world
///
/// = Approach to Message Passing =
/// The state of the world is defined by either
///   1. Inertial Model pose, twist
///      * kinematic data - connectivity graph from Model to each Link
///      * joint angles
///      * joint velocities
///      * Applied forces - Body wrench
///        * relative transform from Body to each collision Geom
/// Or
///   2. Inertial (absolute) Body pose, twist, wrench
///      * relative transform from Body to each collision Geom - constant, so not sent over wire
///      * back compute from canonical body info to get Model pose and twist.
///
/// Chooing (2.) because it matches most physics engines out there
///   and is simpler.
///
/// = Future =
/// Consider impacts on using reduced coordinates / graph (parent/child links) approach
///   constraint and physics solvers.
///
/// = Application =
/// This message is used to do the following:
///   * reconstruct the world and objects for sensor generation
///   * stop / start simulation - need pose, twist, wrench of each body
///   * collision detection - need pose of each collision geometry.  velocity/acceleration if
///
/// = Assumptions =
/// Assuming that each (physics) processor node locally already has
///   * collision information - Trimesh for Geoms, etc
///   * relative transforms from Body to Geom - this is assumed to be fixed, do not send oved wire
///   * inertial information - does not vary in time
///   * visual information - does not vary in time

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WorldState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub name: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: Vec<geometry_msgs::msg::Pose>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub twist: Vec<geometry_msgs::msg::Twist>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub wrench: Vec<geometry_msgs::msg::Wrench>,

}



impl Default for WorldState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::WorldState::default())
  }
}

impl rosidl_runtime_rs::Message for WorldState {
  type RmwMsg = super::msg::rmw::WorldState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        name: msg.name
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        pose: msg.pose
          .into_iter()
          .map(|elem| geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        twist: msg.twist
          .into_iter()
          .map(|elem| geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        wrench: msg.wrench
          .into_iter()
          .map(|elem| geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        name: msg.name
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        pose: msg.pose
          .iter()
          .map(|elem| geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        twist: msg.twist
          .iter()
          .map(|elem| geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        wrench: msg.wrench
          .iter()
          .map(|elem| geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      name: msg.name
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      pose: msg.pose
          .into_iter()
          .map(geometry_msgs::msg::Pose::from_rmw_message)
          .collect(),
      twist: msg.twist
          .into_iter()
          .map(geometry_msgs::msg::Twist::from_rmw_message)
          .collect(),
      wrench: msg.wrench
          .into_iter()
          .map(geometry_msgs::msg::Wrench::from_rmw_message)
          .collect(),
    }
  }
}


