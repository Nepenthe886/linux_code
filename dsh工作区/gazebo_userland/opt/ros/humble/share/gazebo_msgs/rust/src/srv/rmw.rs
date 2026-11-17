#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyBodyWrench_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__ApplyBodyWrench_Request__init(msg: *mut ApplyBodyWrench_Request) -> bool;
    fn gazebo_msgs__srv__ApplyBodyWrench_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ApplyBodyWrench_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__ApplyBodyWrench_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ApplyBodyWrench_Request>);
    fn gazebo_msgs__srv__ApplyBodyWrench_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ApplyBodyWrench_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ApplyBodyWrench_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__ApplyBodyWrench_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyBodyWrench_Request {
    /// Gazebo body to apply wrench (linear force and torque)
    /// wrench is applied in the gazebo world by default
    /// body names are prefixed by model name, e.g. pr2::base_link
    pub body_name: rosidl_runtime_rs::String,

    /// wrench is defined in the reference frame of this entity
    /// use inertial frame if left empty
    /// frame names are bodies prefixed by model name, e.g. pr2::base_link
    pub reference_frame: rosidl_runtime_rs::String,

    /// wrench is defined at this location in the reference frame
    pub reference_point: geometry_msgs::msg::rmw::Point,

    /// wrench applied to the origin of the body
    pub wrench: geometry_msgs::msg::rmw::Wrench,

    /// (optional) wrench application start time (seconds)
    /// if start_time is not specified, or
    /// start_time < current time, start as soon as possible
    pub start_time: builtin_interfaces::msg::rmw::Time,

    /// optional duration of wrench application time (seconds)
    /// if duration < 0, apply wrench continuously without end
    /// if duration = 0, do nothing
    /// if duration < step size, apply wrench
    /// for one step size
    pub duration: builtin_interfaces::msg::rmw::Duration,

}



impl Default for ApplyBodyWrench_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__ApplyBodyWrench_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__ApplyBodyWrench_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ApplyBodyWrench_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyBodyWrench_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyBodyWrench_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyBodyWrench_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ApplyBodyWrench_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ApplyBodyWrench_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/ApplyBodyWrench_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyBodyWrench_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyBodyWrench_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__ApplyBodyWrench_Response__init(msg: *mut ApplyBodyWrench_Response) -> bool;
    fn gazebo_msgs__srv__ApplyBodyWrench_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ApplyBodyWrench_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__ApplyBodyWrench_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ApplyBodyWrench_Response>);
    fn gazebo_msgs__srv__ApplyBodyWrench_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ApplyBodyWrench_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ApplyBodyWrench_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__ApplyBodyWrench_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyBodyWrench_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for ApplyBodyWrench_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__ApplyBodyWrench_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__ApplyBodyWrench_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ApplyBodyWrench_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyBodyWrench_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyBodyWrench_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyBodyWrench_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ApplyBodyWrench_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ApplyBodyWrench_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/ApplyBodyWrench_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyBodyWrench_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyLinkWrench_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__ApplyLinkWrench_Request__init(msg: *mut ApplyLinkWrench_Request) -> bool;
    fn gazebo_msgs__srv__ApplyLinkWrench_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ApplyLinkWrench_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__ApplyLinkWrench_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ApplyLinkWrench_Request>);
    fn gazebo_msgs__srv__ApplyLinkWrench_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ApplyLinkWrench_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ApplyLinkWrench_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__ApplyLinkWrench_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyLinkWrench_Request {
    /// Gazebo link to apply wrench (linear force and torque)
    /// wrench is applied in the gazebo world by default
    /// link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: rosidl_runtime_rs::String,

    /// wrench is defined in the reference frame of this entity
    /// use inertial frame if left empty
    /// frame names are links prefixed by model name, e.g. pr2::base_link
    pub reference_frame: rosidl_runtime_rs::String,

    /// wrench is defined at this location in the reference frame
    pub reference_point: geometry_msgs::msg::rmw::Point,

    /// wrench applied to the origin of the link
    pub wrench: geometry_msgs::msg::rmw::Wrench,

    /// (optional) wrench application start time (seconds)
    /// if start_time is not specified, or
    /// start_time < current time, start as soon as possible
    pub start_time: builtin_interfaces::msg::rmw::Time,

    /// optional duration of wrench application time (seconds)
    /// if duration < 0, apply wrench continuously without end
    /// if duration = 0, do nothing
    /// if duration < step size, apply wrench
    /// for one step size
    pub duration: builtin_interfaces::msg::rmw::Duration,

}



impl Default for ApplyLinkWrench_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__ApplyLinkWrench_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__ApplyLinkWrench_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ApplyLinkWrench_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyLinkWrench_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyLinkWrench_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyLinkWrench_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ApplyLinkWrench_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ApplyLinkWrench_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/ApplyLinkWrench_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyLinkWrench_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyLinkWrench_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__ApplyLinkWrench_Response__init(msg: *mut ApplyLinkWrench_Response) -> bool;
    fn gazebo_msgs__srv__ApplyLinkWrench_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ApplyLinkWrench_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__ApplyLinkWrench_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ApplyLinkWrench_Response>);
    fn gazebo_msgs__srv__ApplyLinkWrench_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ApplyLinkWrench_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ApplyLinkWrench_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__ApplyLinkWrench_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyLinkWrench_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for ApplyLinkWrench_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__ApplyLinkWrench_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__ApplyLinkWrench_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ApplyLinkWrench_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyLinkWrench_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyLinkWrench_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyLinkWrench_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ApplyLinkWrench_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ApplyLinkWrench_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/ApplyLinkWrench_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyLinkWrench_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyJointEffort_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__ApplyJointEffort_Request__init(msg: *mut ApplyJointEffort_Request) -> bool;
    fn gazebo_msgs__srv__ApplyJointEffort_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ApplyJointEffort_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__ApplyJointEffort_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ApplyJointEffort_Request>);
    fn gazebo_msgs__srv__ApplyJointEffort_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ApplyJointEffort_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ApplyJointEffort_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__ApplyJointEffort_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyJointEffort_Request {
    /// joint to apply wrench (linear force and torque)
    pub joint_name: rosidl_runtime_rs::String,

    /// effort to apply
    pub effort: f64,

    /// optional wrench application start time (seconds)
    /// if start_time < current time, start as soon as possible
    pub start_time: builtin_interfaces::msg::rmw::Time,

    /// optional duration of wrench application time (seconds)
    /// if duration < 0, apply wrench continuously without end
    /// if duration = 0, do nothing
    /// if duration < step size, assume step size and
    /// display warning in status_message
    pub duration: builtin_interfaces::msg::rmw::Duration,

}



impl Default for ApplyJointEffort_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__ApplyJointEffort_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__ApplyJointEffort_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ApplyJointEffort_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyJointEffort_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyJointEffort_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyJointEffort_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ApplyJointEffort_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ApplyJointEffort_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/ApplyJointEffort_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyJointEffort_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyJointEffort_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__ApplyJointEffort_Response__init(msg: *mut ApplyJointEffort_Response) -> bool;
    fn gazebo_msgs__srv__ApplyJointEffort_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ApplyJointEffort_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__ApplyJointEffort_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ApplyJointEffort_Response>);
    fn gazebo_msgs__srv__ApplyJointEffort_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ApplyJointEffort_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ApplyJointEffort_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__ApplyJointEffort_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyJointEffort_Response {
    /// return true if effort application is successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for ApplyJointEffort_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__ApplyJointEffort_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__ApplyJointEffort_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ApplyJointEffort_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyJointEffort_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyJointEffort_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__ApplyJointEffort_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ApplyJointEffort_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ApplyJointEffort_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/ApplyJointEffort_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__ApplyJointEffort_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__BodyRequest_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__BodyRequest_Request__init(msg: *mut BodyRequest_Request) -> bool;
    fn gazebo_msgs__srv__BodyRequest_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<BodyRequest_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__BodyRequest_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<BodyRequest_Request>);
    fn gazebo_msgs__srv__BodyRequest_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<BodyRequest_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<BodyRequest_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__BodyRequest_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BodyRequest_Request {
    /// name of the body requested. body names are prefixed by model name, e.g. pr2::base_link
    pub body_name: rosidl_runtime_rs::String,

}



impl Default for BodyRequest_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__BodyRequest_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__BodyRequest_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for BodyRequest_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__BodyRequest_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__BodyRequest_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__BodyRequest_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for BodyRequest_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for BodyRequest_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/BodyRequest_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__BodyRequest_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__BodyRequest_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__BodyRequest_Response__init(msg: *mut BodyRequest_Response) -> bool;
    fn gazebo_msgs__srv__BodyRequest_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<BodyRequest_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__BodyRequest_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<BodyRequest_Response>);
    fn gazebo_msgs__srv__BodyRequest_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<BodyRequest_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<BodyRequest_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__BodyRequest_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BodyRequest_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for BodyRequest_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__BodyRequest_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__BodyRequest_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for BodyRequest_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__BodyRequest_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__BodyRequest_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__BodyRequest_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for BodyRequest_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for BodyRequest_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/BodyRequest_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__BodyRequest_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteEntity_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__DeleteEntity_Request__init(msg: *mut DeleteEntity_Request) -> bool;
    fn gazebo_msgs__srv__DeleteEntity_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DeleteEntity_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__DeleteEntity_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DeleteEntity_Request>);
    fn gazebo_msgs__srv__DeleteEntity_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DeleteEntity_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<DeleteEntity_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__DeleteEntity_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteEntity_Request {
    /// Name of the Gazebo entity to be deleted. This can be either
    /// a model or a light.
    pub name: rosidl_runtime_rs::String,

}



impl Default for DeleteEntity_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__DeleteEntity_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__DeleteEntity_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DeleteEntity_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteEntity_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteEntity_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteEntity_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DeleteEntity_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DeleteEntity_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/DeleteEntity_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteEntity_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteEntity_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__DeleteEntity_Response__init(msg: *mut DeleteEntity_Response) -> bool;
    fn gazebo_msgs__srv__DeleteEntity_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DeleteEntity_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__DeleteEntity_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DeleteEntity_Response>);
    fn gazebo_msgs__srv__DeleteEntity_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DeleteEntity_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<DeleteEntity_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__DeleteEntity_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteEntity_Response {
    /// Return true if deletion is successful.
    pub success: bool,

    /// Comments if available.
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for DeleteEntity_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__DeleteEntity_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__DeleteEntity_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DeleteEntity_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteEntity_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteEntity_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteEntity_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DeleteEntity_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DeleteEntity_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/DeleteEntity_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteEntity_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteLight_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__DeleteLight_Request__init(msg: *mut DeleteLight_Request) -> bool;
    fn gazebo_msgs__srv__DeleteLight_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DeleteLight_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__DeleteLight_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DeleteLight_Request>);
    fn gazebo_msgs__srv__DeleteLight_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DeleteLight_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<DeleteLight_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__DeleteLight_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteLight_Request {
    /// name of the light to be deleted
    pub light_name: rosidl_runtime_rs::String,

}



impl Default for DeleteLight_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__DeleteLight_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__DeleteLight_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DeleteLight_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteLight_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteLight_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteLight_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DeleteLight_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DeleteLight_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/DeleteLight_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteLight_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteLight_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__DeleteLight_Response__init(msg: *mut DeleteLight_Response) -> bool;
    fn gazebo_msgs__srv__DeleteLight_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DeleteLight_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__DeleteLight_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DeleteLight_Response>);
    fn gazebo_msgs__srv__DeleteLight_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DeleteLight_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<DeleteLight_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__DeleteLight_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteLight_Response {
    /// return true if deletion is successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for DeleteLight_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__DeleteLight_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__DeleteLight_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DeleteLight_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteLight_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteLight_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteLight_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DeleteLight_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DeleteLight_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/DeleteLight_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteLight_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteModel_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__DeleteModel_Request__init(msg: *mut DeleteModel_Request) -> bool;
    fn gazebo_msgs__srv__DeleteModel_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DeleteModel_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__DeleteModel_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DeleteModel_Request>);
    fn gazebo_msgs__srv__DeleteModel_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DeleteModel_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<DeleteModel_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__DeleteModel_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteModel_Request {
    /// name of the Gazebo Model to be deleted
    pub model_name: rosidl_runtime_rs::String,

}



impl Default for DeleteModel_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__DeleteModel_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__DeleteModel_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DeleteModel_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteModel_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteModel_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteModel_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DeleteModel_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DeleteModel_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/DeleteModel_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteModel_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteModel_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__DeleteModel_Response__init(msg: *mut DeleteModel_Response) -> bool;
    fn gazebo_msgs__srv__DeleteModel_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DeleteModel_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__DeleteModel_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DeleteModel_Response>);
    fn gazebo_msgs__srv__DeleteModel_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DeleteModel_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<DeleteModel_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__DeleteModel_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteModel_Response {
    /// return true if deletion is successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for DeleteModel_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__DeleteModel_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__DeleteModel_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DeleteModel_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteModel_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteModel_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__DeleteModel_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DeleteModel_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DeleteModel_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/DeleteModel_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__DeleteModel_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetJointProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetJointProperties_Request__init(msg: *mut GetJointProperties_Request) -> bool;
    fn gazebo_msgs__srv__GetJointProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetJointProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetJointProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetJointProperties_Request>);
    fn gazebo_msgs__srv__GetJointProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetJointProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetJointProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetJointProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointProperties_Request {
    /// Scoped name of joint
    pub joint_name: rosidl_runtime_rs::String,

}



impl Default for GetJointProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetJointProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetJointProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetJointProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetJointProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetJointProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetJointProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetJointProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetJointProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetJointProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetJointProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetJointProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetJointProperties_Response__init(msg: *mut GetJointProperties_Response) -> bool;
    fn gazebo_msgs__srv__GetJointProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetJointProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetJointProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetJointProperties_Response>);
    fn gazebo_msgs__srv__GetJointProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetJointProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetJointProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetJointProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointProperties_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub type_: u8,

    /// dynamics properties
    pub damping: rosidl_runtime_rs::Sequence<f64>,

    /// joint state
    pub position: rosidl_runtime_rs::Sequence<f64>,

    /// TODO(chapulina) Rename to velocity
    pub rate: rosidl_runtime_rs::Sequence<f64>,

    /// service return status
    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}

impl GetJointProperties_Response {
    /// single DOF
    pub const REVOLUTE: u8 = 0;

    /// single DOF (revolute w/o limits)
    pub const CONTINUOUS: u8 = 1;

    /// single DOF
    pub const PRISMATIC: u8 = 2;

    /// 0 DOF
    pub const FIXED: u8 = 3;

    /// 3 DOF movement, 0 DOF control
    pub const BALL: u8 = 4;

    /// 2 DOF
    pub const UNIVERSAL: u8 = 5;

}


impl Default for GetJointProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetJointProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetJointProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetJointProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetJointProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetJointProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetJointProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetJointProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetJointProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetJointProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetJointProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetEntityState_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetEntityState_Request__init(msg: *mut GetEntityState_Request) -> bool;
    fn gazebo_msgs__srv__GetEntityState_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetEntityState_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetEntityState_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetEntityState_Request>);
    fn gazebo_msgs__srv__GetEntityState_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetEntityState_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetEntityState_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetEntityState_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetEntityState_Request {
    /// Entity's scoped name.
    /// An entity can be a model, link, collision, light, etc.
    /// Be sure to use gazebo scoped naming notation (e.g.)
    pub name: rosidl_runtime_rs::String,

    /// Return pose and twist relative to this entity.
    /// Leaving empty or "world" will use inertial world frame.
    pub reference_frame: rosidl_runtime_rs::String,

}



impl Default for GetEntityState_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetEntityState_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetEntityState_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetEntityState_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetEntityState_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetEntityState_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetEntityState_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetEntityState_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetEntityState_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetEntityState_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetEntityState_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetEntityState_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetEntityState_Response__init(msg: *mut GetEntityState_Response) -> bool;
    fn gazebo_msgs__srv__GetEntityState_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetEntityState_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetEntityState_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetEntityState_Response>);
    fn gazebo_msgs__srv__GetEntityState_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetEntityState_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetEntityState_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetEntityState_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetEntityState_Response {
    /// Standard metadata for higher-level stamped data types.
    /// * header.stamp Timestamp related to the pose.
    /// * header.frame_id Filled with the relative_frame.
    pub header: std_msgs::msg::rmw::Header,

    /// Contains pose and twist.
    pub state: super::super::msg::rmw::EntityState,

    /// Return true if get was successful. If false, the state contains garbage.
    pub success: bool,

}



impl Default for GetEntityState_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetEntityState_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetEntityState_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetEntityState_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetEntityState_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetEntityState_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetEntityState_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetEntityState_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetEntityState_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetEntityState_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetEntityState_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLightProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetLightProperties_Request__init(msg: *mut GetLightProperties_Request) -> bool;
    fn gazebo_msgs__srv__GetLightProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetLightProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetLightProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetLightProperties_Request>);
    fn gazebo_msgs__srv__GetLightProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetLightProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetLightProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetLightProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLightProperties_Request {
    /// name of Gazebo Light
    pub light_name: rosidl_runtime_rs::String,

}



impl Default for GetLightProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetLightProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetLightProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetLightProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLightProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLightProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLightProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetLightProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetLightProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetLightProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLightProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLightProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetLightProperties_Response__init(msg: *mut GetLightProperties_Response) -> bool;
    fn gazebo_msgs__srv__GetLightProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetLightProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetLightProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetLightProperties_Response>);
    fn gazebo_msgs__srv__GetLightProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetLightProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetLightProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetLightProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLightProperties_Response {
    /// diffuse color as red, green, blue, alpha
    pub diffuse: std_msgs::msg::rmw::ColorRGBA,


    // This member is not documented.
    #[allow(missing_docs)]
    pub attenuation_constant: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub attenuation_linear: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub attenuation_quadratic: f64,

    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for GetLightProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetLightProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetLightProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetLightProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLightProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLightProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLightProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetLightProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetLightProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetLightProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLightProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLinkProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetLinkProperties_Request__init(msg: *mut GetLinkProperties_Request) -> bool;
    fn gazebo_msgs__srv__GetLinkProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetLinkProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetLinkProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetLinkProperties_Request>);
    fn gazebo_msgs__srv__GetLinkProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetLinkProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetLinkProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetLinkProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLinkProperties_Request {
    /// name of link
    /// link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: rosidl_runtime_rs::String,

}



impl Default for GetLinkProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetLinkProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetLinkProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetLinkProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetLinkProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetLinkProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetLinkProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLinkProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLinkProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetLinkProperties_Response__init(msg: *mut GetLinkProperties_Response) -> bool;
    fn gazebo_msgs__srv__GetLinkProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetLinkProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetLinkProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetLinkProperties_Response>);
    fn gazebo_msgs__srv__GetLinkProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetLinkProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetLinkProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetLinkProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLinkProperties_Response {
    /// center of mass location in link frame
    /// and orientation of the moment of inertias
    /// relative to the link frame
    pub com: geometry_msgs::msg::rmw::Pose,

    /// set gravity mode on/off
    pub gravity_mode: bool,

    /// linear mass of link
    pub mass: f64,

    /// moment of inertia
    pub ixx: f64,

    /// moment of inertia
    pub ixy: f64,

    /// moment of inertia
    pub ixz: f64,

    /// moment of inertia
    pub iyy: f64,

    /// moment of inertia
    pub iyz: f64,

    /// moment of inertia
    pub izz: f64,

    /// return true if get info is successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for GetLinkProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetLinkProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetLinkProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetLinkProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetLinkProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetLinkProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetLinkProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLinkProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLinkState_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetLinkState_Request__init(msg: *mut GetLinkState_Request) -> bool;
    fn gazebo_msgs__srv__GetLinkState_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetLinkState_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetLinkState_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetLinkState_Request>);
    fn gazebo_msgs__srv__GetLinkState_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetLinkState_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetLinkState_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetLinkState_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLinkState_Request {
    /// name of link
    /// link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: rosidl_runtime_rs::String,

    /// reference frame of returned information, must be a valid link
    /// if empty, use inertial (gazebo world) frame
    /// reference_frame names are prefixed by model name, e.g. pr2::base_link
    pub reference_frame: rosidl_runtime_rs::String,

}



impl Default for GetLinkState_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetLinkState_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetLinkState_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetLinkState_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkState_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkState_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkState_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetLinkState_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetLinkState_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetLinkState_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLinkState_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLinkState_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetLinkState_Response__init(msg: *mut GetLinkState_Response) -> bool;
    fn gazebo_msgs__srv__GetLinkState_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetLinkState_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetLinkState_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetLinkState_Response>);
    fn gazebo_msgs__srv__GetLinkState_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetLinkState_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetLinkState_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetLinkState_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLinkState_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub link_state: super::super::msg::rmw::LinkState,

    /// return true if get info is successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for GetLinkState_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetLinkState_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetLinkState_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetLinkState_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkState_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkState_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetLinkState_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetLinkState_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetLinkState_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetLinkState_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetLinkState_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelList_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetModelList_Request__init(msg: *mut GetModelList_Request) -> bool;
    fn gazebo_msgs__srv__GetModelList_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetModelList_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetModelList_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetModelList_Request>);
    fn gazebo_msgs__srv__GetModelList_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetModelList_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetModelList_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetModelList_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelList_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetModelList_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetModelList_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetModelList_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetModelList_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelList_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelList_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelList_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetModelList_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetModelList_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetModelList_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelList_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelList_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetModelList_Response__init(msg: *mut GetModelList_Response) -> bool;
    fn gazebo_msgs__srv__GetModelList_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetModelList_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetModelList_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetModelList_Response>);
    fn gazebo_msgs__srv__GetModelList_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetModelList_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetModelList_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetModelList_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelList_Response {
    /// Standard metadata for higher-level stamped data types.
    /// * header.stamp Simulation time when data was collected.
    pub header: std_msgs::msg::rmw::Header,

    /// list of models in the world
    pub model_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// return true if get successful
    pub success: bool,

}



impl Default for GetModelList_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetModelList_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetModelList_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetModelList_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelList_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelList_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelList_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetModelList_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetModelList_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetModelList_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelList_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetModelProperties_Request__init(msg: *mut GetModelProperties_Request) -> bool;
    fn gazebo_msgs__srv__GetModelProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetModelProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetModelProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetModelProperties_Request>);
    fn gazebo_msgs__srv__GetModelProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetModelProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetModelProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetModelProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelProperties_Request {
    /// name of Gazebo Model
    pub model_name: rosidl_runtime_rs::String,

}



impl Default for GetModelProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetModelProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetModelProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetModelProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetModelProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetModelProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetModelProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetModelProperties_Response__init(msg: *mut GetModelProperties_Response) -> bool;
    fn gazebo_msgs__srv__GetModelProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetModelProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetModelProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetModelProperties_Response>);
    fn gazebo_msgs__srv__GetModelProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetModelProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetModelProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetModelProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelProperties_Response {
    /// parent model
    pub parent_model_name: rosidl_runtime_rs::String,

    /// name of canonical link, link names are prefixed by model name, e.g. pr2::base_link
    pub canonical_body_name: rosidl_runtime_rs::String,

    /// list of links, link names are prefixed by model name, e.g. pr2::base_link
    pub body_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// list of collisions
    pub geom_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// list of joints attached to the model
    pub joint_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// list of child models
    pub child_model_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// returns true if model is static
    pub is_static: bool,

    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for GetModelProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetModelProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetModelProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetModelProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetModelProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetModelProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetModelProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelState_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetModelState_Request__init(msg: *mut GetModelState_Request) -> bool;
    fn gazebo_msgs__srv__GetModelState_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetModelState_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetModelState_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetModelState_Request>);
    fn gazebo_msgs__srv__GetModelState_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetModelState_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetModelState_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetModelState_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelState_Request {
    /// name of Gazebo Model
    pub model_name: rosidl_runtime_rs::String,

    /// return pose and twist relative to this entity
    /// an entity can be a model, body, or geom
    /// be sure to use gazebo scoped naming notation (e.g.)
    /// leave empty or "world" will use inertial world frame
    pub relative_entity_name: rosidl_runtime_rs::String,

}



impl Default for GetModelState_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetModelState_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetModelState_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetModelState_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelState_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelState_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelState_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetModelState_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetModelState_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetModelState_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelState_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelState_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetModelState_Response__init(msg: *mut GetModelState_Response) -> bool;
    fn gazebo_msgs__srv__GetModelState_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetModelState_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetModelState_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetModelState_Response>);
    fn gazebo_msgs__srv__GetModelState_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetModelState_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetModelState_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetModelState_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelState_Response {
    /// Standard metadata for higher-level stamped data types.
    /// * header.seq holds the number of requests since the plugin started
    /// * header.stamp timestamp related to the pose
    /// * header.frame_id not used but currently filled with the relative_entity_name
    pub header: std_msgs::msg::rmw::Header,

    /// pose of model in relative entity frame
    pub pose: geometry_msgs::msg::rmw::Pose,

    /// twist of model in relative entity frame
    pub twist: geometry_msgs::msg::rmw::Twist,

    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for GetModelState_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetModelState_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetModelState_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetModelState_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelState_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelState_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetModelState_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetModelState_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetModelState_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetModelState_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetModelState_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetPhysicsProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetPhysicsProperties_Request__init(msg: *mut GetPhysicsProperties_Request) -> bool;
    fn gazebo_msgs__srv__GetPhysicsProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetPhysicsProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetPhysicsProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetPhysicsProperties_Request>);
    fn gazebo_msgs__srv__GetPhysicsProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetPhysicsProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetPhysicsProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetPhysicsProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetPhysicsProperties_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetPhysicsProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetPhysicsProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetPhysicsProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetPhysicsProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetPhysicsProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetPhysicsProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetPhysicsProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetPhysicsProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetPhysicsProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetPhysicsProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetPhysicsProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetPhysicsProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetPhysicsProperties_Response__init(msg: *mut GetPhysicsProperties_Response) -> bool;
    fn gazebo_msgs__srv__GetPhysicsProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetPhysicsProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetPhysicsProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetPhysicsProperties_Response>);
    fn gazebo_msgs__srv__GetPhysicsProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetPhysicsProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetPhysicsProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetPhysicsProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetPhysicsProperties_Response {
    /// dt in seconds
    pub time_step: f64,

    /// true if physics engine is paused
    pub pause: bool,

    /// throttle maximum physics update rate
    pub max_update_rate: f64,

    /// gravity vector (e.g. earth ~[0,0,-9.81])
    pub gravity: geometry_msgs::msg::rmw::Vector3,

    /// contains physics configurations pertaining to ODE
    pub ode_config: super::super::msg::rmw::ODEPhysics,

    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for GetPhysicsProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetPhysicsProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetPhysicsProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetPhysicsProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetPhysicsProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetPhysicsProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetPhysicsProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetPhysicsProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetPhysicsProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetPhysicsProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetPhysicsProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetWorldProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetWorldProperties_Request__init(msg: *mut GetWorldProperties_Request) -> bool;
    fn gazebo_msgs__srv__GetWorldProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetWorldProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetWorldProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetWorldProperties_Request>);
    fn gazebo_msgs__srv__GetWorldProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetWorldProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetWorldProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetWorldProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetWorldProperties_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetWorldProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetWorldProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetWorldProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetWorldProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetWorldProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetWorldProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetWorldProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetWorldProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetWorldProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetWorldProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetWorldProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetWorldProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__GetWorldProperties_Response__init(msg: *mut GetWorldProperties_Response) -> bool;
    fn gazebo_msgs__srv__GetWorldProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetWorldProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__GetWorldProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetWorldProperties_Response>);
    fn gazebo_msgs__srv__GetWorldProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetWorldProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetWorldProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__GetWorldProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetWorldProperties_Response {
    /// current sim time
    pub sim_time: f64,

    /// list of models in the world
    pub model_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// if X is used
    pub rendering_enabled: bool,

    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for GetWorldProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__GetWorldProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__GetWorldProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetWorldProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetWorldProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetWorldProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__GetWorldProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetWorldProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetWorldProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/GetWorldProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__GetWorldProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__JointRequest_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__JointRequest_Request__init(msg: *mut JointRequest_Request) -> bool;
    fn gazebo_msgs__srv__JointRequest_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JointRequest_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__JointRequest_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JointRequest_Request>);
    fn gazebo_msgs__srv__JointRequest_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JointRequest_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<JointRequest_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__JointRequest_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JointRequest_Request {
    /// name of the joint requested
    pub joint_name: rosidl_runtime_rs::String,

}



impl Default for JointRequest_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__JointRequest_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__JointRequest_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JointRequest_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__JointRequest_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__JointRequest_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__JointRequest_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JointRequest_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JointRequest_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/JointRequest_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__JointRequest_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__JointRequest_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__JointRequest_Response__init(msg: *mut JointRequest_Response) -> bool;
    fn gazebo_msgs__srv__JointRequest_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JointRequest_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__JointRequest_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JointRequest_Response>);
    fn gazebo_msgs__srv__JointRequest_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JointRequest_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<JointRequest_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__JointRequest_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JointRequest_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for JointRequest_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__JointRequest_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__JointRequest_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JointRequest_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__JointRequest_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__JointRequest_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__JointRequest_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JointRequest_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JointRequest_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/JointRequest_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__JointRequest_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__LinkRequest_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__LinkRequest_Request__init(msg: *mut LinkRequest_Request) -> bool;
    fn gazebo_msgs__srv__LinkRequest_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LinkRequest_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__LinkRequest_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LinkRequest_Request>);
    fn gazebo_msgs__srv__LinkRequest_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LinkRequest_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<LinkRequest_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__LinkRequest_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LinkRequest_Request {
    /// name of the link requested. link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: rosidl_runtime_rs::String,

}



impl Default for LinkRequest_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__LinkRequest_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__LinkRequest_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LinkRequest_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__LinkRequest_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__LinkRequest_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__LinkRequest_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LinkRequest_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LinkRequest_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/LinkRequest_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__LinkRequest_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__LinkRequest_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__LinkRequest_Response__init(msg: *mut LinkRequest_Response) -> bool;
    fn gazebo_msgs__srv__LinkRequest_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<LinkRequest_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__LinkRequest_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<LinkRequest_Response>);
    fn gazebo_msgs__srv__LinkRequest_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<LinkRequest_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<LinkRequest_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__LinkRequest_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LinkRequest_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LinkRequest_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__LinkRequest_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__LinkRequest_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for LinkRequest_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__LinkRequest_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__LinkRequest_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__LinkRequest_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for LinkRequest_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for LinkRequest_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/LinkRequest_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__LinkRequest_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetEntityState_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetEntityState_Request__init(msg: *mut SetEntityState_Request) -> bool;
    fn gazebo_msgs__srv__SetEntityState_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetEntityState_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetEntityState_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetEntityState_Request>);
    fn gazebo_msgs__srv__SetEntityState_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetEntityState_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetEntityState_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetEntityState_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetEntityState_Request {
    /// Entity state to set to.
    /// Be sure to fill all fields, values of zero have meaning.
    pub state: super::super::msg::rmw::EntityState,

}



impl Default for SetEntityState_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetEntityState_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetEntityState_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetEntityState_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetEntityState_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetEntityState_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetEntityState_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetEntityState_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetEntityState_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetEntityState_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetEntityState_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetEntityState_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetEntityState_Response__init(msg: *mut SetEntityState_Response) -> bool;
    fn gazebo_msgs__srv__SetEntityState_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetEntityState_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetEntityState_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetEntityState_Response>);
    fn gazebo_msgs__srv__SetEntityState_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetEntityState_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetEntityState_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetEntityState_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetEntityState_Response {
    /// Return true if setting state was successful.
    pub success: bool,

}



impl Default for SetEntityState_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetEntityState_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetEntityState_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetEntityState_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetEntityState_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetEntityState_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetEntityState_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetEntityState_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetEntityState_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetEntityState_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetEntityState_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetJointProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetJointProperties_Request__init(msg: *mut SetJointProperties_Request) -> bool;
    fn gazebo_msgs__srv__SetJointProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetJointProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetJointProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetJointProperties_Request>);
    fn gazebo_msgs__srv__SetJointProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetJointProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetJointProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetJointProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointProperties_Request {
    /// name of joint
    pub joint_name: rosidl_runtime_rs::String,

    /// access to ODE joint dynamics properties
    pub ode_joint_config: super::super::msg::rmw::ODEJointProperties,

}



impl Default for SetJointProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetJointProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetJointProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetJointProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetJointProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetJointProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetJointProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetJointProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetJointProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetJointProperties_Response__init(msg: *mut SetJointProperties_Response) -> bool;
    fn gazebo_msgs__srv__SetJointProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetJointProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetJointProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetJointProperties_Response>);
    fn gazebo_msgs__srv__SetJointProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetJointProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetJointProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetJointProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointProperties_Response {
    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SetJointProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetJointProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetJointProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetJointProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetJointProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetJointProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetJointProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetJointProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetJointTrajectory_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetJointTrajectory_Request__init(msg: *mut SetJointTrajectory_Request) -> bool;
    fn gazebo_msgs__srv__SetJointTrajectory_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetJointTrajectory_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetJointTrajectory_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetJointTrajectory_Request>);
    fn gazebo_msgs__srv__SetJointTrajectory_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetJointTrajectory_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetJointTrajectory_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetJointTrajectory_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointTrajectory_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub model_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_trajectory: trajectory_msgs::msg::rmw::JointTrajectory,


    // This member is not documented.
    #[allow(missing_docs)]
    pub model_pose: geometry_msgs::msg::rmw::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub set_model_pose: bool,

    /// defaults to false
    pub disable_physics_updates: bool,

}



impl Default for SetJointTrajectory_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetJointTrajectory_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetJointTrajectory_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetJointTrajectory_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointTrajectory_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointTrajectory_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointTrajectory_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetJointTrajectory_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetJointTrajectory_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetJointTrajectory_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetJointTrajectory_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetJointTrajectory_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetJointTrajectory_Response__init(msg: *mut SetJointTrajectory_Response) -> bool;
    fn gazebo_msgs__srv__SetJointTrajectory_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetJointTrajectory_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetJointTrajectory_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetJointTrajectory_Response>);
    fn gazebo_msgs__srv__SetJointTrajectory_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetJointTrajectory_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetJointTrajectory_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetJointTrajectory_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointTrajectory_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SetJointTrajectory_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetJointTrajectory_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetJointTrajectory_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetJointTrajectory_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointTrajectory_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointTrajectory_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetJointTrajectory_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetJointTrajectory_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetJointTrajectory_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetJointTrajectory_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetJointTrajectory_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLightProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetLightProperties_Request__init(msg: *mut SetLightProperties_Request) -> bool;
    fn gazebo_msgs__srv__SetLightProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetLightProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetLightProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetLightProperties_Request>);
    fn gazebo_msgs__srv__SetLightProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetLightProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetLightProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetLightProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLightProperties_Request {
    /// name of Gazebo Light
    pub light_name: rosidl_runtime_rs::String,

    /// diffuse color as red, green, blue, alpha
    pub diffuse: std_msgs::msg::rmw::ColorRGBA,


    // This member is not documented.
    #[allow(missing_docs)]
    pub attenuation_constant: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub attenuation_linear: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub attenuation_quadratic: f64,

}



impl Default for SetLightProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetLightProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetLightProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetLightProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLightProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLightProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLightProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetLightProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetLightProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetLightProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLightProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLightProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetLightProperties_Response__init(msg: *mut SetLightProperties_Response) -> bool;
    fn gazebo_msgs__srv__SetLightProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetLightProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetLightProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetLightProperties_Response>);
    fn gazebo_msgs__srv__SetLightProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetLightProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetLightProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetLightProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLightProperties_Response {
    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SetLightProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetLightProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetLightProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetLightProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLightProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLightProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLightProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetLightProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetLightProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetLightProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLightProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLinkProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetLinkProperties_Request__init(msg: *mut SetLinkProperties_Request) -> bool;
    fn gazebo_msgs__srv__SetLinkProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetLinkProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetLinkProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetLinkProperties_Request>);
    fn gazebo_msgs__srv__SetLinkProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetLinkProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetLinkProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetLinkProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLinkProperties_Request {
    /// name of link
    /// link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: rosidl_runtime_rs::String,

    /// center of mass location in link frame
    /// and orientation of the moment of inertias
    /// relative to the link frame
    pub com: geometry_msgs::msg::rmw::Pose,

    /// set gravity mode on/off
    pub gravity_mode: bool,

    /// linear mass of link
    pub mass: f64,

    /// moment of inertia
    pub ixx: f64,

    /// moment of inertia
    pub ixy: f64,

    /// moment of inertia
    pub ixz: f64,

    /// moment of inertia
    pub iyy: f64,

    /// moment of inertia
    pub iyz: f64,

    /// moment of inertia
    pub izz: f64,

}



impl Default for SetLinkProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetLinkProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetLinkProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetLinkProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetLinkProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetLinkProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetLinkProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLinkProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLinkProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetLinkProperties_Response__init(msg: *mut SetLinkProperties_Response) -> bool;
    fn gazebo_msgs__srv__SetLinkProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetLinkProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetLinkProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetLinkProperties_Response>);
    fn gazebo_msgs__srv__SetLinkProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetLinkProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetLinkProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetLinkProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLinkProperties_Response {
    /// return true if get info is successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SetLinkProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetLinkProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetLinkProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetLinkProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetLinkProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetLinkProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetLinkProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLinkProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLinkState_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetLinkState_Request__init(msg: *mut SetLinkState_Request) -> bool;
    fn gazebo_msgs__srv__SetLinkState_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetLinkState_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetLinkState_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetLinkState_Request>);
    fn gazebo_msgs__srv__SetLinkState_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetLinkState_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetLinkState_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetLinkState_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLinkState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub link_state: super::super::msg::rmw::LinkState,

}



impl Default for SetLinkState_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetLinkState_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetLinkState_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetLinkState_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkState_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkState_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkState_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetLinkState_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetLinkState_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetLinkState_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLinkState_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLinkState_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetLinkState_Response__init(msg: *mut SetLinkState_Response) -> bool;
    fn gazebo_msgs__srv__SetLinkState_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetLinkState_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetLinkState_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetLinkState_Response>);
    fn gazebo_msgs__srv__SetLinkState_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetLinkState_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetLinkState_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetLinkState_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLinkState_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SetLinkState_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetLinkState_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetLinkState_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetLinkState_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkState_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkState_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetLinkState_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetLinkState_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetLinkState_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetLinkState_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetLinkState_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetModelConfiguration_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetModelConfiguration_Request__init(msg: *mut SetModelConfiguration_Request) -> bool;
    fn gazebo_msgs__srv__SetModelConfiguration_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetModelConfiguration_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetModelConfiguration_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetModelConfiguration_Request>);
    fn gazebo_msgs__srv__SetModelConfiguration_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetModelConfiguration_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetModelConfiguration_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetModelConfiguration_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModelConfiguration_Request {
    /// model to set state
    pub model_name: rosidl_runtime_rs::String,

    /// UNUSED
    pub urdf_param_name: rosidl_runtime_rs::String,

    /// list of joints to set positions.  if joint is not listed here, preserve current position.
    pub joint_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

    /// set to this position.
    pub joint_positions: rosidl_runtime_rs::Sequence<f64>,

}



impl Default for SetModelConfiguration_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetModelConfiguration_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetModelConfiguration_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetModelConfiguration_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelConfiguration_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelConfiguration_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelConfiguration_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetModelConfiguration_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetModelConfiguration_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetModelConfiguration_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetModelConfiguration_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetModelConfiguration_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetModelConfiguration_Response__init(msg: *mut SetModelConfiguration_Response) -> bool;
    fn gazebo_msgs__srv__SetModelConfiguration_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetModelConfiguration_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetModelConfiguration_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetModelConfiguration_Response>);
    fn gazebo_msgs__srv__SetModelConfiguration_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetModelConfiguration_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetModelConfiguration_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetModelConfiguration_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModelConfiguration_Response {
    /// return true if setting state successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SetModelConfiguration_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetModelConfiguration_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetModelConfiguration_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetModelConfiguration_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelConfiguration_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelConfiguration_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelConfiguration_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetModelConfiguration_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetModelConfiguration_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetModelConfiguration_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetModelConfiguration_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetModelState_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetModelState_Request__init(msg: *mut SetModelState_Request) -> bool;
    fn gazebo_msgs__srv__SetModelState_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetModelState_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetModelState_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetModelState_Request>);
    fn gazebo_msgs__srv__SetModelState_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetModelState_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetModelState_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetModelState_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModelState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub model_state: super::super::msg::rmw::ModelState,

}



impl Default for SetModelState_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetModelState_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetModelState_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetModelState_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelState_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelState_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelState_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetModelState_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetModelState_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetModelState_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetModelState_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetModelState_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetModelState_Response__init(msg: *mut SetModelState_Response) -> bool;
    fn gazebo_msgs__srv__SetModelState_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetModelState_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetModelState_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetModelState_Response>);
    fn gazebo_msgs__srv__SetModelState_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetModelState_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetModelState_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetModelState_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModelState_Response {
    /// return true if setting state successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SetModelState_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetModelState_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetModelState_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetModelState_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelState_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelState_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetModelState_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetModelState_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetModelState_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetModelState_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetModelState_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetPhysicsProperties_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetPhysicsProperties_Request__init(msg: *mut SetPhysicsProperties_Request) -> bool;
    fn gazebo_msgs__srv__SetPhysicsProperties_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetPhysicsProperties_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetPhysicsProperties_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetPhysicsProperties_Request>);
    fn gazebo_msgs__srv__SetPhysicsProperties_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetPhysicsProperties_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetPhysicsProperties_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetPhysicsProperties_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetPhysicsProperties_Request {
    /// dt in seconds
    pub time_step: f64,

    /// throttle maximum physics update rate
    pub max_update_rate: f64,

    /// gravity vector (e.g. earth ~[0,0,-9.81])
    pub gravity: geometry_msgs::msg::rmw::Vector3,

    /// configurations for ODE
    pub ode_config: super::super::msg::rmw::ODEPhysics,

}



impl Default for SetPhysicsProperties_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetPhysicsProperties_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetPhysicsProperties_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetPhysicsProperties_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetPhysicsProperties_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetPhysicsProperties_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetPhysicsProperties_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetPhysicsProperties_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetPhysicsProperties_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetPhysicsProperties_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetPhysicsProperties_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetPhysicsProperties_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SetPhysicsProperties_Response__init(msg: *mut SetPhysicsProperties_Response) -> bool;
    fn gazebo_msgs__srv__SetPhysicsProperties_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetPhysicsProperties_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SetPhysicsProperties_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetPhysicsProperties_Response>);
    fn gazebo_msgs__srv__SetPhysicsProperties_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetPhysicsProperties_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetPhysicsProperties_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SetPhysicsProperties_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetPhysicsProperties_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SetPhysicsProperties_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SetPhysicsProperties_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SetPhysicsProperties_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetPhysicsProperties_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetPhysicsProperties_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetPhysicsProperties_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SetPhysicsProperties_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetPhysicsProperties_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetPhysicsProperties_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SetPhysicsProperties_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SetPhysicsProperties_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SpawnEntity_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SpawnEntity_Request__init(msg: *mut SpawnEntity_Request) -> bool;
    fn gazebo_msgs__srv__SpawnEntity_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SpawnEntity_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SpawnEntity_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SpawnEntity_Request>);
    fn gazebo_msgs__srv__SpawnEntity_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SpawnEntity_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SpawnEntity_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SpawnEntity_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpawnEntity_Request {
    /// Name of the entity to be spawned (optional).
    pub name: rosidl_runtime_rs::String,

    /// Entity XML description as a string, either URDF or SDF.
    pub xml: rosidl_runtime_rs::String,

    /// Spawn robot and all ROS interfaces under this namespace
    pub robot_namespace: rosidl_runtime_rs::String,

    /// Initial entity pose.
    pub initial_pose: geometry_msgs::msg::rmw::Pose,

    /// initial_pose is defined relative to the frame of this entity.
    /// If left empty or "world" or "map", then gazebo world frame is
    /// used.
    /// If non-existent entity is specified, an error is returned
    /// and the entity is not spawned.
    pub reference_frame: rosidl_runtime_rs::String,

}



impl Default for SpawnEntity_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SpawnEntity_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SpawnEntity_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SpawnEntity_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnEntity_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnEntity_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnEntity_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SpawnEntity_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SpawnEntity_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SpawnEntity_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SpawnEntity_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SpawnEntity_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SpawnEntity_Response__init(msg: *mut SpawnEntity_Response) -> bool;
    fn gazebo_msgs__srv__SpawnEntity_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SpawnEntity_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SpawnEntity_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SpawnEntity_Response>);
    fn gazebo_msgs__srv__SpawnEntity_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SpawnEntity_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SpawnEntity_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SpawnEntity_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpawnEntity_Response {
    /// Return true if spawned successfully.
    pub success: bool,

    /// Comments if available.
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SpawnEntity_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SpawnEntity_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SpawnEntity_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SpawnEntity_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnEntity_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnEntity_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnEntity_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SpawnEntity_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SpawnEntity_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SpawnEntity_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SpawnEntity_Response() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SpawnModel_Request() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SpawnModel_Request__init(msg: *mut SpawnModel_Request) -> bool;
    fn gazebo_msgs__srv__SpawnModel_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SpawnModel_Request>, size: usize) -> bool;
    fn gazebo_msgs__srv__SpawnModel_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SpawnModel_Request>);
    fn gazebo_msgs__srv__SpawnModel_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SpawnModel_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SpawnModel_Request>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SpawnModel_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpawnModel_Request {
    /// name of the model to be spawn
    pub model_name: rosidl_runtime_rs::String,

    /// this should be an urdf or gazebo xml
    pub model_xml: rosidl_runtime_rs::String,

    /// spawn robot and all ROS interfaces under this namespace
    pub robot_namespace: rosidl_runtime_rs::String,

    /// only applied to canonical body
    pub initial_pose: geometry_msgs::msg::rmw::Pose,

    /// initial_pose is defined relative to the frame of this model/body
    /// if left empty or "world", then gazebo world frame is used
    /// if non-existent model/body is specified, an error is returned
    ///   and the model is not spawned
    pub reference_frame: rosidl_runtime_rs::String,

}



impl Default for SpawnModel_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SpawnModel_Request__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SpawnModel_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SpawnModel_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnModel_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnModel_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnModel_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SpawnModel_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SpawnModel_Request where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SpawnModel_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SpawnModel_Request() }
  }
}


#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SpawnModel_Response() -> *const std::ffi::c_void;
}

#[link(name = "gazebo_msgs__rosidl_generator_c")]
extern "C" {
    fn gazebo_msgs__srv__SpawnModel_Response__init(msg: *mut SpawnModel_Response) -> bool;
    fn gazebo_msgs__srv__SpawnModel_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SpawnModel_Response>, size: usize) -> bool;
    fn gazebo_msgs__srv__SpawnModel_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SpawnModel_Response>);
    fn gazebo_msgs__srv__SpawnModel_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SpawnModel_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SpawnModel_Response>) -> bool;
}

// Corresponds to gazebo_msgs__srv__SpawnModel_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpawnModel_Response {
    /// return true if spawn successful
    pub success: bool,

    /// comments if available
    pub status_message: rosidl_runtime_rs::String,

}



impl Default for SpawnModel_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !gazebo_msgs__srv__SpawnModel_Response__init(&mut msg as *mut _) {
        panic!("Call to gazebo_msgs__srv__SpawnModel_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SpawnModel_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnModel_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnModel_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { gazebo_msgs__srv__SpawnModel_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SpawnModel_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SpawnModel_Response where Self: Sized {
  const TYPE_NAME: &'static str = "gazebo_msgs/srv/SpawnModel_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__gazebo_msgs__srv__SpawnModel_Response() }
  }
}






#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__ApplyBodyWrench() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__ApplyBodyWrench
#[allow(missing_docs, non_camel_case_types)]
pub struct ApplyBodyWrench;

impl rosidl_runtime_rs::Service for ApplyBodyWrench {
    type Request = ApplyBodyWrench_Request;
    type Response = ApplyBodyWrench_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__ApplyBodyWrench() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__ApplyLinkWrench() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__ApplyLinkWrench
#[allow(missing_docs, non_camel_case_types)]
pub struct ApplyLinkWrench;

impl rosidl_runtime_rs::Service for ApplyLinkWrench {
    type Request = ApplyLinkWrench_Request;
    type Response = ApplyLinkWrench_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__ApplyLinkWrench() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__ApplyJointEffort() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__ApplyJointEffort
#[allow(missing_docs, non_camel_case_types)]
pub struct ApplyJointEffort;

impl rosidl_runtime_rs::Service for ApplyJointEffort {
    type Request = ApplyJointEffort_Request;
    type Response = ApplyJointEffort_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__ApplyJointEffort() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__BodyRequest() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__BodyRequest
#[allow(missing_docs, non_camel_case_types)]
pub struct BodyRequest;

impl rosidl_runtime_rs::Service for BodyRequest {
    type Request = BodyRequest_Request;
    type Response = BodyRequest_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__BodyRequest() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__DeleteEntity() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__DeleteEntity
#[allow(missing_docs, non_camel_case_types)]
pub struct DeleteEntity;

impl rosidl_runtime_rs::Service for DeleteEntity {
    type Request = DeleteEntity_Request;
    type Response = DeleteEntity_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__DeleteEntity() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__DeleteLight() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__DeleteLight
#[allow(missing_docs, non_camel_case_types)]
pub struct DeleteLight;

impl rosidl_runtime_rs::Service for DeleteLight {
    type Request = DeleteLight_Request;
    type Response = DeleteLight_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__DeleteLight() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__DeleteModel() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__DeleteModel
#[allow(missing_docs, non_camel_case_types)]
pub struct DeleteModel;

impl rosidl_runtime_rs::Service for DeleteModel {
    type Request = DeleteModel_Request;
    type Response = DeleteModel_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__DeleteModel() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetJointProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetJointProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct GetJointProperties;

impl rosidl_runtime_rs::Service for GetJointProperties {
    type Request = GetJointProperties_Request;
    type Response = GetJointProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetJointProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetEntityState() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetEntityState
#[allow(missing_docs, non_camel_case_types)]
pub struct GetEntityState;

impl rosidl_runtime_rs::Service for GetEntityState {
    type Request = GetEntityState_Request;
    type Response = GetEntityState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetEntityState() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetLightProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetLightProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct GetLightProperties;

impl rosidl_runtime_rs::Service for GetLightProperties {
    type Request = GetLightProperties_Request;
    type Response = GetLightProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetLightProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetLinkProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetLinkProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct GetLinkProperties;

impl rosidl_runtime_rs::Service for GetLinkProperties {
    type Request = GetLinkProperties_Request;
    type Response = GetLinkProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetLinkProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetLinkState() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetLinkState
#[allow(missing_docs, non_camel_case_types)]
pub struct GetLinkState;

impl rosidl_runtime_rs::Service for GetLinkState {
    type Request = GetLinkState_Request;
    type Response = GetLinkState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetLinkState() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetModelList() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetModelList
#[allow(missing_docs, non_camel_case_types)]
pub struct GetModelList;

impl rosidl_runtime_rs::Service for GetModelList {
    type Request = GetModelList_Request;
    type Response = GetModelList_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetModelList() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetModelProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetModelProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct GetModelProperties;

impl rosidl_runtime_rs::Service for GetModelProperties {
    type Request = GetModelProperties_Request;
    type Response = GetModelProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetModelProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetModelState() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetModelState
#[allow(missing_docs, non_camel_case_types)]
pub struct GetModelState;

impl rosidl_runtime_rs::Service for GetModelState {
    type Request = GetModelState_Request;
    type Response = GetModelState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetModelState() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetPhysicsProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetPhysicsProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct GetPhysicsProperties;

impl rosidl_runtime_rs::Service for GetPhysicsProperties {
    type Request = GetPhysicsProperties_Request;
    type Response = GetPhysicsProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetPhysicsProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetWorldProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__GetWorldProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct GetWorldProperties;

impl rosidl_runtime_rs::Service for GetWorldProperties {
    type Request = GetWorldProperties_Request;
    type Response = GetWorldProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__GetWorldProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__JointRequest() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__JointRequest
#[allow(missing_docs, non_camel_case_types)]
pub struct JointRequest;

impl rosidl_runtime_rs::Service for JointRequest {
    type Request = JointRequest_Request;
    type Response = JointRequest_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__JointRequest() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__LinkRequest() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__LinkRequest
#[allow(missing_docs, non_camel_case_types)]
pub struct LinkRequest;

impl rosidl_runtime_rs::Service for LinkRequest {
    type Request = LinkRequest_Request;
    type Response = LinkRequest_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__LinkRequest() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetEntityState() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SetEntityState
#[allow(missing_docs, non_camel_case_types)]
pub struct SetEntityState;

impl rosidl_runtime_rs::Service for SetEntityState {
    type Request = SetEntityState_Request;
    type Response = SetEntityState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetEntityState() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetJointProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SetJointProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct SetJointProperties;

impl rosidl_runtime_rs::Service for SetJointProperties {
    type Request = SetJointProperties_Request;
    type Response = SetJointProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetJointProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetJointTrajectory() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SetJointTrajectory
#[allow(missing_docs, non_camel_case_types)]
pub struct SetJointTrajectory;

impl rosidl_runtime_rs::Service for SetJointTrajectory {
    type Request = SetJointTrajectory_Request;
    type Response = SetJointTrajectory_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetJointTrajectory() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetLightProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SetLightProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct SetLightProperties;

impl rosidl_runtime_rs::Service for SetLightProperties {
    type Request = SetLightProperties_Request;
    type Response = SetLightProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetLightProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetLinkProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SetLinkProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct SetLinkProperties;

impl rosidl_runtime_rs::Service for SetLinkProperties {
    type Request = SetLinkProperties_Request;
    type Response = SetLinkProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetLinkProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetLinkState() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SetLinkState
#[allow(missing_docs, non_camel_case_types)]
pub struct SetLinkState;

impl rosidl_runtime_rs::Service for SetLinkState {
    type Request = SetLinkState_Request;
    type Response = SetLinkState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetLinkState() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetModelConfiguration() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SetModelConfiguration
#[allow(missing_docs, non_camel_case_types)]
pub struct SetModelConfiguration;

impl rosidl_runtime_rs::Service for SetModelConfiguration {
    type Request = SetModelConfiguration_Request;
    type Response = SetModelConfiguration_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetModelConfiguration() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetModelState() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SetModelState
#[allow(missing_docs, non_camel_case_types)]
pub struct SetModelState;

impl rosidl_runtime_rs::Service for SetModelState {
    type Request = SetModelState_Request;
    type Response = SetModelState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetModelState() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetPhysicsProperties() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SetPhysicsProperties
#[allow(missing_docs, non_camel_case_types)]
pub struct SetPhysicsProperties;

impl rosidl_runtime_rs::Service for SetPhysicsProperties {
    type Request = SetPhysicsProperties_Request;
    type Response = SetPhysicsProperties_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SetPhysicsProperties() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SpawnEntity() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SpawnEntity
#[allow(missing_docs, non_camel_case_types)]
pub struct SpawnEntity;

impl rosidl_runtime_rs::Service for SpawnEntity {
    type Request = SpawnEntity_Request;
    type Response = SpawnEntity_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SpawnEntity() }
    }
}




#[link(name = "gazebo_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SpawnModel() -> *const std::ffi::c_void;
}

// Corresponds to gazebo_msgs__srv__SpawnModel
#[allow(missing_docs, non_camel_case_types)]
pub struct SpawnModel;

impl rosidl_runtime_rs::Service for SpawnModel {
    type Request = SpawnModel_Request;
    type Response = SpawnModel_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__gazebo_msgs__srv__SpawnModel() }
    }
}


