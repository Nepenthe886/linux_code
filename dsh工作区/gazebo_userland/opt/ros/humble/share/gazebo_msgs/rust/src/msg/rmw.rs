#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ContactState() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__ContactState__init(msg: *mut ContactState) -> bool;
    fn gazebo_msgs__msg__ContactState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ContactState>, size: usize) -> bool;
    fn gazebo_msgs__msg__ContactState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ContactState>);
    fn gazebo_msgs__msg__ContactState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ContactState>, out_seq: *mut rosidl_runtime_rs::Sequence<ContactState>) -> bool;
}

// Corresponds to gazebo_msgs__msg__ContactState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ContactState {
    /// text info on this contact
    pub info: rosidl_runtime_rs::String,

    /// name of contact collision1
    pub collision1_name: rosidl_runtime_rs::String,

    /// name of contact collision2
    pub collision2_name: rosidl_runtime_rs::String,

    /// list of forces/torques
    pub wrenches: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Wrench>,

    /// sum of forces/torques in every DOF
    pub total_wrench: geometry_msgs::msg::rmw::Wrench,

    /// list of contact position
    pub contact_positions: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Vector3>,

    /// list of contact normals
    pub contact_normals: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Vector3>,

    /// list of penetration depths
    pub depths: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for ContactState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__ContactState__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__ContactState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ContactState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ContactState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ContactState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ContactState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ContactState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ContactState where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/ContactState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ContactState() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ContactsState() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__ContactsState__init(msg: *mut ContactsState) -> bool;
    fn gazebo_msgs__msg__ContactsState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ContactsState>, size: usize) -> bool;
    fn gazebo_msgs__msg__ContactsState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ContactsState>);
    fn gazebo_msgs__msg__ContactsState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ContactsState>, out_seq: *mut rosidl_runtime_rs::Sequence<ContactsState>) -> bool;
}

// Corresponds to gazebo_msgs__msg__ContactsState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ContactsState {
    /// stamp
    pub header: std_msgs::msg::rmw::Header,

    /// array of geom pairs in contact
    pub states: rosidl_runtime_rs::Sequence<super::super::msg::rmw::ContactState>,

}



impl Default for ContactsState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__ContactsState__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__ContactsState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ContactsState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ContactsState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ContactsState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ContactsState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ContactsState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ContactsState where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/ContactsState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ContactsState() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__EntityState() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__EntityState__init(msg: *mut EntityState) -> bool;
    fn gazebo_msgs__msg__EntityState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<EntityState>, size: usize) -> bool;
    fn gazebo_msgs__msg__EntityState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<EntityState>);
    fn gazebo_msgs__msg__EntityState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<EntityState>, out_seq: *mut rosidl_runtime_rs::Sequence<EntityState>) -> bool;
}

// Corresponds to gazebo_msgs__msg__EntityState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Holds an entity's pose and twist

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EntityState {
    /// Entity's scoped name.
    /// An entity can be a model, link, collision, light, etc.
    /// Be sure to use gazebo scoped naming notation (e.g.)
    pub name: rosidl_runtime_rs::String,

    /// Pose in reference frame.
    pub pose: geometry_msgs::msg::rmw::Pose,

    /// Twist in reference frame.
    pub twist: geometry_msgs::msg::rmw::Twist,

    /// Pose/twist are expressed relative to the frame of this entity.
    /// Leaving empty or "world" defaults to inertial world frame.
    pub reference_frame: rosidl_runtime_rs::String,

}



impl Default for EntityState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__EntityState__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__EntityState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for EntityState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__EntityState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__EntityState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__EntityState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for EntityState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for EntityState where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/EntityState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__EntityState() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__LinkState() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__LinkState__init(msg: *mut LinkState) -> bool;
    fn gazebo_msgs__msg__LinkState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LinkState>, size: usize) -> bool;
    fn gazebo_msgs__msg__LinkState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LinkState>);
    fn gazebo_msgs__msg__LinkState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LinkState>, out_seq: *mut rosidl_runtime_rs::Sequence<LinkState>) -> bool;
}

// Corresponds to gazebo_msgs__msg__LinkState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Deprecated, kept for ROS 1 bridge.
/// Use EntityState
/// @todo: FIXME: sets pose and twist of a link.  All children link poses/twists of the URDF tree are not updated accordingly, but should be.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LinkState {
    /// link name, link_names are in gazebo scoped name notation,
    pub link_name: rosidl_runtime_rs::String,

    /// desired pose in reference frame
    pub pose: geometry_msgs::msg::rmw::Pose,

    /// desired twist in reference frame
    pub twist: geometry_msgs::msg::rmw::Twist,

    /// set pose/twist relative to the frame of this link/body
    /// leave empty or "world" or "map" defaults to world-frame
    pub reference_frame: rosidl_runtime_rs::String,

}



impl Default for LinkState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__LinkState__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__LinkState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LinkState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__LinkState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__LinkState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__LinkState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LinkState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LinkState where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/LinkState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__LinkState() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__LinkStates() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__LinkStates__init(msg: *mut LinkStates) -> bool;
    fn gazebo_msgs__msg__LinkStates__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LinkStates>, size: usize) -> bool;
    fn gazebo_msgs__msg__LinkStates__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LinkStates>);
    fn gazebo_msgs__msg__LinkStates__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LinkStates>, out_seq: *mut rosidl_runtime_rs::Sequence<LinkStates>) -> bool;
}

// Corresponds to gazebo_msgs__msg__LinkStates
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// broadcast all link states in world frame

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LinkStates {
    /// link names
    pub name: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// desired pose in world frame
    pub pose: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Pose>,

    /// desired twist in world frame
    pub twist: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Twist>,

}



impl Default for LinkStates {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__LinkStates__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__LinkStates__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LinkStates {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__LinkStates__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__LinkStates__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__LinkStates__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LinkStates {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LinkStates where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/LinkStates";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__LinkStates() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ModelState() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__ModelState__init(msg: *mut ModelState) -> bool;
    fn gazebo_msgs__msg__ModelState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ModelState>, size: usize) -> bool;
    fn gazebo_msgs__msg__ModelState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ModelState>);
    fn gazebo_msgs__msg__ModelState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ModelState>, out_seq: *mut rosidl_runtime_rs::Sequence<ModelState>) -> bool;
}

// Corresponds to gazebo_msgs__msg__ModelState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Deprecated, kept for ROS 1 bridge.
/// Use EntityState
/// Set Gazebo Model pose and twist

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ModelState {
    /// model to set state (pose and twist)
    pub model_name: rosidl_runtime_rs::String,

    /// desired pose in reference frame
    pub pose: geometry_msgs::msg::rmw::Pose,

    /// desired twist in reference frame
    pub twist: geometry_msgs::msg::rmw::Twist,

    /// set pose/twist relative to the frame of this entity (Body/Model)
    /// leave empty or "world" or "map" defaults to world-frame
    pub reference_frame: rosidl_runtime_rs::String,

}



impl Default for ModelState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__ModelState__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__ModelState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ModelState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ModelState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ModelState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ModelState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ModelState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ModelState where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/ModelState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ModelState() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ModelStates() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__ModelStates__init(msg: *mut ModelStates) -> bool;
    fn gazebo_msgs__msg__ModelStates__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ModelStates>, size: usize) -> bool;
    fn gazebo_msgs__msg__ModelStates__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ModelStates>);
    fn gazebo_msgs__msg__ModelStates__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ModelStates>, out_seq: *mut rosidl_runtime_rs::Sequence<ModelStates>) -> bool;
}

// Corresponds to gazebo_msgs__msg__ModelStates
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// broadcast all model states in world frame

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ModelStates {
    /// model names
    pub name: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// desired pose in world frame
    pub pose: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Pose>,

    /// desired twist in world frame
    pub twist: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Twist>,

}



impl Default for ModelStates {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__ModelStates__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__ModelStates__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ModelStates {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ModelStates__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ModelStates__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ModelStates__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ModelStates {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ModelStates where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/ModelStates";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ModelStates() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ODEJointProperties() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__ODEJointProperties__init(msg: *mut ODEJointProperties) -> bool;
    fn gazebo_msgs__msg__ODEJointProperties__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ODEJointProperties>, size: usize) -> bool;
    fn gazebo_msgs__msg__ODEJointProperties__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ODEJointProperties>);
    fn gazebo_msgs__msg__ODEJointProperties__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ODEJointProperties>, out_seq: *mut rosidl_runtime_rs::Sequence<ODEJointProperties>) -> bool;
}

// Corresponds to gazebo_msgs__msg__ODEJointProperties
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// access to low level joint properties, change these at your own risk

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ODEJointProperties {
    /// joint damping
    pub damping: rosidl_runtime_rs::Sequence<f64>,

    /// joint limit
    pub hi_stop: rosidl_runtime_rs::Sequence<f64>,

    /// joint limit
    pub lo_stop: rosidl_runtime_rs::Sequence<f64>,

    /// set joint erp
    pub erp: rosidl_runtime_rs::Sequence<f64>,

    /// set joint cfm
    pub cfm: rosidl_runtime_rs::Sequence<f64>,

    /// set joint erp for joint limit "contact" joint
    pub stop_erp: rosidl_runtime_rs::Sequence<f64>,

    /// set joint cfm for joint limit "contact" joint
    pub stop_cfm: rosidl_runtime_rs::Sequence<f64>,

    /// joint fudge_factor applied at limits, see ODE manual for info.
    pub fudge_factor: rosidl_runtime_rs::Sequence<f64>,

    /// ode joint param fmax
    pub fmax: rosidl_runtime_rs::Sequence<f64>,

    /// ode joint param vel
    pub vel: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for ODEJointProperties {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__ODEJointProperties__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__ODEJointProperties__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ODEJointProperties {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ODEJointProperties__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ODEJointProperties__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ODEJointProperties__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ODEJointProperties {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ODEJointProperties where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/ODEJointProperties";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ODEJointProperties() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ODEPhysics() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__ODEPhysics__init(msg: *mut ODEPhysics) -> bool;
    fn gazebo_msgs__msg__ODEPhysics__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ODEPhysics>, size: usize) -> bool;
    fn gazebo_msgs__msg__ODEPhysics__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ODEPhysics>);
    fn gazebo_msgs__msg__ODEPhysics__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ODEPhysics>, out_seq: *mut rosidl_runtime_rs::Sequence<ODEPhysics>) -> bool;
}

// Corresponds to gazebo_msgs__msg__ODEPhysics
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__ODEPhysics__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__ODEPhysics__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ODEPhysics {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ODEPhysics__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ODEPhysics__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__ODEPhysics__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ODEPhysics {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ODEPhysics where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/ODEPhysics";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__ODEPhysics() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__PerformanceMetrics() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__PerformanceMetrics__init(msg: *mut PerformanceMetrics) -> bool;
    fn gazebo_msgs__msg__PerformanceMetrics__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PerformanceMetrics>, size: usize) -> bool;
    fn gazebo_msgs__msg__PerformanceMetrics__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PerformanceMetrics>);
    fn gazebo_msgs__msg__PerformanceMetrics__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PerformanceMetrics>, out_seq: *mut rosidl_runtime_rs::Sequence<PerformanceMetrics>) -> bool;
}

// Corresponds to gazebo_msgs__msg__PerformanceMetrics
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PerformanceMetrics {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub real_time_factor: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sensors: rosidl_runtime_rs::Sequence<super::super::msg::rmw::SensorPerformanceMetric>,

}



impl Default for PerformanceMetrics {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__PerformanceMetrics__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__PerformanceMetrics__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PerformanceMetrics {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__PerformanceMetrics__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__PerformanceMetrics__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__PerformanceMetrics__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PerformanceMetrics {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PerformanceMetrics where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/PerformanceMetrics";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__PerformanceMetrics() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__SensorPerformanceMetric() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__SensorPerformanceMetric__init(msg: *mut SensorPerformanceMetric) -> bool;
    fn gazebo_msgs__msg__SensorPerformanceMetric__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SensorPerformanceMetric>, size: usize) -> bool;
    fn gazebo_msgs__msg__SensorPerformanceMetric__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SensorPerformanceMetric>);
    fn gazebo_msgs__msg__SensorPerformanceMetric__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SensorPerformanceMetric>, out_seq: *mut rosidl_runtime_rs::Sequence<SensorPerformanceMetric>) -> bool;
}

// Corresponds to gazebo_msgs__msg__SensorPerformanceMetric
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SensorPerformanceMetric {

    // This member is not documented.
    #[allow(missing_docs)]
    pub name: rosidl_runtime_rs::String,


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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__SensorPerformanceMetric__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__SensorPerformanceMetric__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SensorPerformanceMetric {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__SensorPerformanceMetric__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__SensorPerformanceMetric__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__SensorPerformanceMetric__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SensorPerformanceMetric {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SensorPerformanceMetric where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/SensorPerformanceMetric";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__SensorPerformanceMetric() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__WheelSlip() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__WheelSlip__init(msg: *mut WheelSlip) -> bool;
    fn gazebo_msgs__msg__WheelSlip__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WheelSlip>, size: usize) -> bool;
    fn gazebo_msgs__msg__WheelSlip__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WheelSlip>);
    fn gazebo_msgs__msg__WheelSlip__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WheelSlip>, out_seq: *mut rosidl_runtime_rs::Sequence<WheelSlip>) -> bool;
}

// Corresponds to gazebo_msgs__msg__WheelSlip
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

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

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WheelSlip {

    // This member is not documented.
    #[allow(missing_docs)]
    pub name: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lateral_slip: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub longitudinal_slip: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for WheelSlip {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__WheelSlip__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__WheelSlip__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WheelSlip {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__WheelSlip__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__WheelSlip__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__WheelSlip__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WheelSlip {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WheelSlip where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/WheelSlip";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__WheelSlip() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__WorldState() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__msg__WorldState__init(msg: *mut WorldState) -> bool;
    fn gazebo_msgs__msg__WorldState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WorldState>, size: usize) -> bool;
    fn gazebo_msgs__msg__WorldState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WorldState>);
    fn gazebo_msgs__msg__WorldState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WorldState>, out_seq: *mut rosidl_runtime_rs::Sequence<WorldState>) -> bool;
}

// Corresponds to gazebo_msgs__msg__WorldState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

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

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WorldState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub name: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Pose>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub twist: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Twist>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub wrench: rosidl_runtime_rs::Sequence<geometry_msgs::msg::rmw::Wrench>,

}



impl Default for WorldState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__msg__WorldState__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__msg__WorldState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WorldState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__WorldState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__WorldState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__msg__WorldState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WorldState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WorldState where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/msg/WorldState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__msg__WorldState() }
  }
}


