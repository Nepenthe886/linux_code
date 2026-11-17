#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to gazebo_msgs__srv__ApplyBodyWrench_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyBodyWrench_Request {
    /// Gazebo body to apply wrench (linear force and torque)
    /// wrench is applied in the gazebo world by default
    /// body names are prefixed by model name, e.g. pr2::base_link
    pub body_name: std::string::String,

    /// wrench is defined in the reference frame of this entity
    /// use inertial frame if left empty
    /// frame names are bodies prefixed by model name, e.g. pr2::base_link
    pub reference_frame: std::string::String,

    /// wrench is defined at this location in the reference frame
    pub reference_point: geometry_msgs::msg::Point,

    /// wrench applied to the origin of the body
    pub wrench: geometry_msgs::msg::Wrench,

    /// (optional) wrench application start time (seconds)
    /// if start_time is not specified, or
    /// start_time < current time, start as soon as possible
    pub start_time: builtin_interfaces::msg::Time,

    /// optional duration of wrench application time (seconds)
    /// if duration < 0, apply wrench continuously without end
    /// if duration = 0, do nothing
    /// if duration < step size, apply wrench
    /// for one step size
    pub duration: builtin_interfaces::msg::Duration,

}



impl Default for ApplyBodyWrench_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ApplyBodyWrench_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ApplyBodyWrench_Request {
  type RmwMsg = super::srv::rmw::ApplyBodyWrench_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        body_name: msg.body_name.as_str().into(),
        reference_frame: msg.reference_frame.as_str().into(),
        reference_point: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Owned(msg.reference_point)).into_owned(),
        wrench: geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Owned(msg.wrench)).into_owned(),
        start_time: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.start_time)).into_owned(),
        duration: builtin_interfaces::msg::Duration::into_rmw_message(std::borrow::Cow::Owned(msg.duration)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        body_name: msg.body_name.as_str().into(),
        reference_frame: msg.reference_frame.as_str().into(),
        reference_point: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Borrowed(&msg.reference_point)).into_owned(),
        wrench: geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Borrowed(&msg.wrench)).into_owned(),
        start_time: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.start_time)).into_owned(),
        duration: builtin_interfaces::msg::Duration::into_rmw_message(std::borrow::Cow::Borrowed(&msg.duration)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      body_name: msg.body_name.to_string(),
      reference_frame: msg.reference_frame.to_string(),
      reference_point: geometry_msgs::msg::Point::from_rmw_message(msg.reference_point),
      wrench: geometry_msgs::msg::Wrench::from_rmw_message(msg.wrench),
      start_time: builtin_interfaces::msg::Time::from_rmw_message(msg.start_time),
      duration: builtin_interfaces::msg::Duration::from_rmw_message(msg.duration),
    }
  }
}


// Corresponds to gazebo_msgs__srv__ApplyBodyWrench_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyBodyWrench_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for ApplyBodyWrench_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ApplyBodyWrench_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ApplyBodyWrench_Response {
  type RmwMsg = super::srv::rmw::ApplyBodyWrench_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__ApplyLinkWrench_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyLinkWrench_Request {
    /// Gazebo link to apply wrench (linear force and torque)
    /// wrench is applied in the gazebo world by default
    /// link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: std::string::String,

    /// wrench is defined in the reference frame of this entity
    /// use inertial frame if left empty
    /// frame names are links prefixed by model name, e.g. pr2::base_link
    pub reference_frame: std::string::String,

    /// wrench is defined at this location in the reference frame
    pub reference_point: geometry_msgs::msg::Point,

    /// wrench applied to the origin of the link
    pub wrench: geometry_msgs::msg::Wrench,

    /// (optional) wrench application start time (seconds)
    /// if start_time is not specified, or
    /// start_time < current time, start as soon as possible
    pub start_time: builtin_interfaces::msg::Time,

    /// optional duration of wrench application time (seconds)
    /// if duration < 0, apply wrench continuously without end
    /// if duration = 0, do nothing
    /// if duration < step size, apply wrench
    /// for one step size
    pub duration: builtin_interfaces::msg::Duration,

}



impl Default for ApplyLinkWrench_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ApplyLinkWrench_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ApplyLinkWrench_Request {
  type RmwMsg = super::srv::rmw::ApplyLinkWrench_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
        reference_frame: msg.reference_frame.as_str().into(),
        reference_point: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Owned(msg.reference_point)).into_owned(),
        wrench: geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Owned(msg.wrench)).into_owned(),
        start_time: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.start_time)).into_owned(),
        duration: builtin_interfaces::msg::Duration::into_rmw_message(std::borrow::Cow::Owned(msg.duration)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
        reference_frame: msg.reference_frame.as_str().into(),
        reference_point: geometry_msgs::msg::Point::into_rmw_message(std::borrow::Cow::Borrowed(&msg.reference_point)).into_owned(),
        wrench: geometry_msgs::msg::Wrench::into_rmw_message(std::borrow::Cow::Borrowed(&msg.wrench)).into_owned(),
        start_time: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.start_time)).into_owned(),
        duration: builtin_interfaces::msg::Duration::into_rmw_message(std::borrow::Cow::Borrowed(&msg.duration)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      link_name: msg.link_name.to_string(),
      reference_frame: msg.reference_frame.to_string(),
      reference_point: geometry_msgs::msg::Point::from_rmw_message(msg.reference_point),
      wrench: geometry_msgs::msg::Wrench::from_rmw_message(msg.wrench),
      start_time: builtin_interfaces::msg::Time::from_rmw_message(msg.start_time),
      duration: builtin_interfaces::msg::Duration::from_rmw_message(msg.duration),
    }
  }
}


// Corresponds to gazebo_msgs__srv__ApplyLinkWrench_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyLinkWrench_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for ApplyLinkWrench_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ApplyLinkWrench_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ApplyLinkWrench_Response {
  type RmwMsg = super::srv::rmw::ApplyLinkWrench_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__ApplyJointEffort_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyJointEffort_Request {
    /// joint to apply wrench (linear force and torque)
    pub joint_name: std::string::String,

    /// effort to apply
    pub effort: f64,

    /// optional wrench application start time (seconds)
    /// if start_time < current time, start as soon as possible
    pub start_time: builtin_interfaces::msg::Time,

    /// optional duration of wrench application time (seconds)
    /// if duration < 0, apply wrench continuously without end
    /// if duration = 0, do nothing
    /// if duration < step size, assume step size and
    /// display warning in status_message
    pub duration: builtin_interfaces::msg::Duration,

}



impl Default for ApplyJointEffort_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ApplyJointEffort_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ApplyJointEffort_Request {
  type RmwMsg = super::srv::rmw::ApplyJointEffort_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name.as_str().into(),
        effort: msg.effort,
        start_time: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.start_time)).into_owned(),
        duration: builtin_interfaces::msg::Duration::into_rmw_message(std::borrow::Cow::Owned(msg.duration)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name.as_str().into(),
      effort: msg.effort,
        start_time: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.start_time)).into_owned(),
        duration: builtin_interfaces::msg::Duration::into_rmw_message(std::borrow::Cow::Borrowed(&msg.duration)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_name: msg.joint_name.to_string(),
      effort: msg.effort,
      start_time: builtin_interfaces::msg::Time::from_rmw_message(msg.start_time),
      duration: builtin_interfaces::msg::Duration::from_rmw_message(msg.duration),
    }
  }
}


// Corresponds to gazebo_msgs__srv__ApplyJointEffort_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ApplyJointEffort_Response {
    /// return true if effort application is successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for ApplyJointEffort_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ApplyJointEffort_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ApplyJointEffort_Response {
  type RmwMsg = super::srv::rmw::ApplyJointEffort_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__BodyRequest_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BodyRequest_Request {
    /// name of the body requested. body names are prefixed by model name, e.g. pr2::base_link
    pub body_name: std::string::String,

}



impl Default for BodyRequest_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::BodyRequest_Request::default())
  }
}

impl rosidl_runtime_rs::Message for BodyRequest_Request {
  type RmwMsg = super::srv::rmw::BodyRequest_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        body_name: msg.body_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        body_name: msg.body_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      body_name: msg.body_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__BodyRequest_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct BodyRequest_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for BodyRequest_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::BodyRequest_Response::default())
  }
}

impl rosidl_runtime_rs::Message for BodyRequest_Response {
  type RmwMsg = super::srv::rmw::BodyRequest_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to gazebo_msgs__srv__DeleteEntity_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteEntity_Request {
    /// Name of the Gazebo entity to be deleted. This can be either
    /// a model or a light.
    pub name: std::string::String,

}



impl Default for DeleteEntity_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DeleteEntity_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DeleteEntity_Request {
  type RmwMsg = super::srv::rmw::DeleteEntity_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__DeleteEntity_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteEntity_Response {
    /// Return true if deletion is successful.
    pub success: bool,

    /// Comments if available.
    pub status_message: std::string::String,

}



impl Default for DeleteEntity_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DeleteEntity_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DeleteEntity_Response {
  type RmwMsg = super::srv::rmw::DeleteEntity_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__DeleteLight_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteLight_Request {
    /// name of the light to be deleted
    pub light_name: std::string::String,

}



impl Default for DeleteLight_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DeleteLight_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DeleteLight_Request {
  type RmwMsg = super::srv::rmw::DeleteLight_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        light_name: msg.light_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        light_name: msg.light_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      light_name: msg.light_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__DeleteLight_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteLight_Response {
    /// return true if deletion is successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for DeleteLight_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DeleteLight_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DeleteLight_Response {
  type RmwMsg = super::srv::rmw::DeleteLight_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__DeleteModel_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteModel_Request {
    /// name of the Gazebo Model to be deleted
    pub model_name: std::string::String,

}



impl Default for DeleteModel_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DeleteModel_Request::default())
  }
}

impl rosidl_runtime_rs::Message for DeleteModel_Request {
  type RmwMsg = super::srv::rmw::DeleteModel_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model_name: msg.model_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__DeleteModel_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeleteModel_Response {
    /// return true if deletion is successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for DeleteModel_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::DeleteModel_Response::default())
  }
}

impl rosidl_runtime_rs::Message for DeleteModel_Response {
  type RmwMsg = super::srv::rmw::DeleteModel_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetJointProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointProperties_Request {
    /// Scoped name of joint
    pub joint_name: std::string::String,

}



impl Default for GetJointProperties_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetJointProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetJointProperties_Request {
  type RmwMsg = super::srv::rmw::GetJointProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_name: msg.joint_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetJointProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointProperties_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub type_: u8,

    /// dynamics properties
    pub damping: Vec<f64>,

    /// joint state
    pub position: Vec<f64>,

    /// TODO(chapulina) Rename to velocity
    pub rate: Vec<f64>,

    /// service return status
    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetJointProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetJointProperties_Response {
  type RmwMsg = super::srv::rmw::GetJointProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        type_: msg.type_,
        damping: msg.damping.as_slice().into(),
        position: msg.position.as_slice().into(),
        rate: msg.rate.as_slice().into(),
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      type_: msg.type_,
        damping: msg.damping.as_slice().into(),
        position: msg.position.as_slice().into(),
        rate: msg.rate.as_slice().into(),
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      type_: msg.type_,
      damping: msg.damping.into(),
      position: msg.position.into(),
      rate: msg.rate.into(),
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetEntityState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetEntityState_Request {
    /// Entity's scoped name.
    /// An entity can be a model, link, collision, light, etc.
    /// Be sure to use gazebo scoped naming notation (e.g.)
    pub name: std::string::String,

    /// Return pose and twist relative to this entity.
    /// Leaving empty or "world" will use inertial world frame.
    pub reference_frame: std::string::String,

}



impl Default for GetEntityState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetEntityState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetEntityState_Request {
  type RmwMsg = super::srv::rmw::GetEntityState_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        reference_frame: msg.reference_frame.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        reference_frame: msg.reference_frame.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      reference_frame: msg.reference_frame.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetEntityState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetEntityState_Response {
    /// Standard metadata for higher-level stamped data types.
    /// * header.stamp Timestamp related to the pose.
    /// * header.frame_id Filled with the relative_frame.
    pub header: std_msgs::msg::Header,

    /// Contains pose and twist.
    pub state: super::msg::EntityState,

    /// Return true if get was successful. If false, the state contains garbage.
    pub success: bool,

}



impl Default for GetEntityState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetEntityState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetEntityState_Response {
  type RmwMsg = super::srv::rmw::GetEntityState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        state: super::msg::EntityState::into_rmw_message(std::borrow::Cow::Owned(msg.state)).into_owned(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        state: super::msg::EntityState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.state)).into_owned(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      state: super::msg::EntityState::from_rmw_message(msg.state),
      success: msg.success,
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetLightProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLightProperties_Request {
    /// name of Gazebo Light
    pub light_name: std::string::String,

}



impl Default for GetLightProperties_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetLightProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetLightProperties_Request {
  type RmwMsg = super::srv::rmw::GetLightProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        light_name: msg.light_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        light_name: msg.light_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      light_name: msg.light_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetLightProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLightProperties_Response {
    /// diffuse color as red, green, blue, alpha
    pub diffuse: std_msgs::msg::ColorRGBA,


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
    pub status_message: std::string::String,

}



impl Default for GetLightProperties_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetLightProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetLightProperties_Response {
  type RmwMsg = super::srv::rmw::GetLightProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        diffuse: std_msgs::msg::ColorRGBA::into_rmw_message(std::borrow::Cow::Owned(msg.diffuse)).into_owned(),
        attenuation_constant: msg.attenuation_constant,
        attenuation_linear: msg.attenuation_linear,
        attenuation_quadratic: msg.attenuation_quadratic,
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        diffuse: std_msgs::msg::ColorRGBA::into_rmw_message(std::borrow::Cow::Borrowed(&msg.diffuse)).into_owned(),
      attenuation_constant: msg.attenuation_constant,
      attenuation_linear: msg.attenuation_linear,
      attenuation_quadratic: msg.attenuation_quadratic,
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      diffuse: std_msgs::msg::ColorRGBA::from_rmw_message(msg.diffuse),
      attenuation_constant: msg.attenuation_constant,
      attenuation_linear: msg.attenuation_linear,
      attenuation_quadratic: msg.attenuation_quadratic,
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetLinkProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLinkProperties_Request {
    /// name of link
    /// link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: std::string::String,

}



impl Default for GetLinkProperties_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetLinkProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetLinkProperties_Request {
  type RmwMsg = super::srv::rmw::GetLinkProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      link_name: msg.link_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetLinkProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLinkProperties_Response {
    /// center of mass location in link frame
    /// and orientation of the moment of inertias
    /// relative to the link frame
    pub com: geometry_msgs::msg::Pose,

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
    pub status_message: std::string::String,

}



impl Default for GetLinkProperties_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetLinkProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetLinkProperties_Response {
  type RmwMsg = super::srv::rmw::GetLinkProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        com: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.com)).into_owned(),
        gravity_mode: msg.gravity_mode,
        mass: msg.mass,
        ixx: msg.ixx,
        ixy: msg.ixy,
        ixz: msg.ixz,
        iyy: msg.iyy,
        iyz: msg.iyz,
        izz: msg.izz,
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        com: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.com)).into_owned(),
      gravity_mode: msg.gravity_mode,
      mass: msg.mass,
      ixx: msg.ixx,
      ixy: msg.ixy,
      ixz: msg.ixz,
      iyy: msg.iyy,
      iyz: msg.iyz,
      izz: msg.izz,
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      com: geometry_msgs::msg::Pose::from_rmw_message(msg.com),
      gravity_mode: msg.gravity_mode,
      mass: msg.mass,
      ixx: msg.ixx,
      ixy: msg.ixy,
      ixz: msg.ixz,
      iyy: msg.iyy,
      iyz: msg.iyz,
      izz: msg.izz,
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetLinkState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLinkState_Request {
    /// name of link
    /// link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: std::string::String,

    /// reference frame of returned information, must be a valid link
    /// if empty, use inertial (gazebo world) frame
    /// reference_frame names are prefixed by model name, e.g. pr2::base_link
    pub reference_frame: std::string::String,

}



impl Default for GetLinkState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetLinkState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetLinkState_Request {
  type RmwMsg = super::srv::rmw::GetLinkState_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
        reference_frame: msg.reference_frame.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
        reference_frame: msg.reference_frame.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      link_name: msg.link_name.to_string(),
      reference_frame: msg.reference_frame.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetLinkState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetLinkState_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub link_state: super::msg::LinkState,

    /// return true if get info is successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for GetLinkState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetLinkState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetLinkState_Response {
  type RmwMsg = super::srv::rmw::GetLinkState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_state: super::msg::LinkState::into_rmw_message(std::borrow::Cow::Owned(msg.link_state)).into_owned(),
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_state: super::msg::LinkState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.link_state)).into_owned(),
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      link_state: super::msg::LinkState::from_rmw_message(msg.link_state),
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetModelList_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelList_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetModelList_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetModelList_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetModelList_Request {
  type RmwMsg = super::srv::rmw::GetModelList_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetModelList_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelList_Response {
    /// Standard metadata for higher-level stamped data types.
    /// * header.stamp Simulation time when data was collected.
    pub header: std_msgs::msg::Header,

    /// list of models in the world
    pub model_names: Vec<std::string::String>,

    /// return true if get successful
    pub success: bool,

}



impl Default for GetModelList_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetModelList_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetModelList_Response {
  type RmwMsg = super::srv::rmw::GetModelList_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        model_names: msg.model_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        model_names: msg.model_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      model_names: msg.model_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      success: msg.success,
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetModelProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelProperties_Request {
    /// name of Gazebo Model
    pub model_name: std::string::String,

}



impl Default for GetModelProperties_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetModelProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetModelProperties_Request {
  type RmwMsg = super::srv::rmw::GetModelProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model_name: msg.model_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetModelProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelProperties_Response {
    /// parent model
    pub parent_model_name: std::string::String,

    /// name of canonical link, link names are prefixed by model name, e.g. pr2::base_link
    pub canonical_body_name: std::string::String,

    /// list of links, link names are prefixed by model name, e.g. pr2::base_link
    pub body_names: Vec<std::string::String>,

    /// list of collisions
    pub geom_names: Vec<std::string::String>,

    /// list of joints attached to the model
    pub joint_names: Vec<std::string::String>,

    /// list of child models
    pub child_model_names: Vec<std::string::String>,

    /// returns true if model is static
    pub is_static: bool,

    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for GetModelProperties_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetModelProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetModelProperties_Response {
  type RmwMsg = super::srv::rmw::GetModelProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        parent_model_name: msg.parent_model_name.as_str().into(),
        canonical_body_name: msg.canonical_body_name.as_str().into(),
        body_names: msg.body_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        geom_names: msg.geom_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        child_model_names: msg.child_model_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        is_static: msg.is_static,
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        parent_model_name: msg.parent_model_name.as_str().into(),
        canonical_body_name: msg.canonical_body_name.as_str().into(),
        body_names: msg.body_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        geom_names: msg.geom_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        joint_names: msg.joint_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        child_model_names: msg.child_model_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      is_static: msg.is_static,
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      parent_model_name: msg.parent_model_name.to_string(),
      canonical_body_name: msg.canonical_body_name.to_string(),
      body_names: msg.body_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      geom_names: msg.geom_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      child_model_names: msg.child_model_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      is_static: msg.is_static,
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetModelState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelState_Request {
    /// name of Gazebo Model
    pub model_name: std::string::String,

    /// return pose and twist relative to this entity
    /// an entity can be a model, body, or geom
    /// be sure to use gazebo scoped naming notation (e.g.)
    /// leave empty or "world" will use inertial world frame
    pub relative_entity_name: std::string::String,

}



impl Default for GetModelState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetModelState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetModelState_Request {
  type RmwMsg = super::srv::rmw::GetModelState_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        relative_entity_name: msg.relative_entity_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        relative_entity_name: msg.relative_entity_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model_name: msg.model_name.to_string(),
      relative_entity_name: msg.relative_entity_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetModelState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetModelState_Response {
    /// Standard metadata for higher-level stamped data types.
    /// * header.seq holds the number of requests since the plugin started
    /// * header.stamp timestamp related to the pose
    /// * header.frame_id not used but currently filled with the relative_entity_name
    pub header: std_msgs::msg::Header,

    /// pose of model in relative entity frame
    pub pose: geometry_msgs::msg::Pose,

    /// twist of model in relative entity frame
    pub twist: geometry_msgs::msg::Twist,

    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for GetModelState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetModelState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetModelState_Response {
  type RmwMsg = super::srv::rmw::GetModelState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Owned(msg.twist)).into_owned(),
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
        twist: geometry_msgs::msg::Twist::into_rmw_message(std::borrow::Cow::Borrowed(&msg.twist)).into_owned(),
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      twist: geometry_msgs::msg::Twist::from_rmw_message(msg.twist),
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetPhysicsProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetPhysicsProperties_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetPhysicsProperties_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetPhysicsProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetPhysicsProperties_Request {
  type RmwMsg = super::srv::rmw::GetPhysicsProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetPhysicsProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetPhysicsProperties_Response {
    /// dt in seconds
    pub time_step: f64,

    /// true if physics engine is paused
    pub pause: bool,

    /// throttle maximum physics update rate
    pub max_update_rate: f64,

    /// gravity vector (e.g. earth ~[0,0,-9.81])
    pub gravity: geometry_msgs::msg::Vector3,

    /// contains physics configurations pertaining to ODE
    pub ode_config: super::msg::ODEPhysics,

    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for GetPhysicsProperties_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetPhysicsProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetPhysicsProperties_Response {
  type RmwMsg = super::srv::rmw::GetPhysicsProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        time_step: msg.time_step,
        pause: msg.pause,
        max_update_rate: msg.max_update_rate,
        gravity: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Owned(msg.gravity)).into_owned(),
        ode_config: super::msg::ODEPhysics::into_rmw_message(std::borrow::Cow::Owned(msg.ode_config)).into_owned(),
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      time_step: msg.time_step,
      pause: msg.pause,
      max_update_rate: msg.max_update_rate,
        gravity: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Borrowed(&msg.gravity)).into_owned(),
        ode_config: super::msg::ODEPhysics::into_rmw_message(std::borrow::Cow::Borrowed(&msg.ode_config)).into_owned(),
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      time_step: msg.time_step,
      pause: msg.pause,
      max_update_rate: msg.max_update_rate,
      gravity: geometry_msgs::msg::Vector3::from_rmw_message(msg.gravity),
      ode_config: super::msg::ODEPhysics::from_rmw_message(msg.ode_config),
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetWorldProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetWorldProperties_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetWorldProperties_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetWorldProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetWorldProperties_Request {
  type RmwMsg = super::srv::rmw::GetWorldProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to gazebo_msgs__srv__GetWorldProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetWorldProperties_Response {
    /// current sim time
    pub sim_time: f64,

    /// list of models in the world
    pub model_names: Vec<std::string::String>,

    /// if X is used
    pub rendering_enabled: bool,

    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for GetWorldProperties_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetWorldProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetWorldProperties_Response {
  type RmwMsg = super::srv::rmw::GetWorldProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        sim_time: msg.sim_time,
        model_names: msg.model_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        rendering_enabled: msg.rendering_enabled,
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      sim_time: msg.sim_time,
        model_names: msg.model_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      rendering_enabled: msg.rendering_enabled,
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      sim_time: msg.sim_time,
      model_names: msg.model_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      rendering_enabled: msg.rendering_enabled,
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__JointRequest_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JointRequest_Request {
    /// name of the joint requested
    pub joint_name: std::string::String,

}



impl Default for JointRequest_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::JointRequest_Request::default())
  }
}

impl rosidl_runtime_rs::Message for JointRequest_Request {
  type RmwMsg = super::srv::rmw::JointRequest_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_name: msg.joint_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__JointRequest_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JointRequest_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for JointRequest_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::JointRequest_Response::default())
  }
}

impl rosidl_runtime_rs::Message for JointRequest_Response {
  type RmwMsg = super::srv::rmw::JointRequest_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to gazebo_msgs__srv__LinkRequest_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LinkRequest_Request {
    /// name of the link requested. link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: std::string::String,

}



impl Default for LinkRequest_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LinkRequest_Request::default())
  }
}

impl rosidl_runtime_rs::Message for LinkRequest_Request {
  type RmwMsg = super::srv::rmw::LinkRequest_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      link_name: msg.link_name.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__LinkRequest_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct LinkRequest_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for LinkRequest_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::LinkRequest_Response::default())
  }
}

impl rosidl_runtime_rs::Message for LinkRequest_Response {
  type RmwMsg = super::srv::rmw::LinkRequest_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetEntityState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetEntityState_Request {
    /// Entity state to set to.
    /// Be sure to fill all fields, values of zero have meaning.
    pub state: super::msg::EntityState,

}



impl Default for SetEntityState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetEntityState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetEntityState_Request {
  type RmwMsg = super::srv::rmw::SetEntityState_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        state: super::msg::EntityState::into_rmw_message(std::borrow::Cow::Owned(msg.state)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        state: super::msg::EntityState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.state)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      state: super::msg::EntityState::from_rmw_message(msg.state),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetEntityState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetEntityState_Response {
    /// Return true if setting state was successful.
    pub success: bool,

}



impl Default for SetEntityState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetEntityState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetEntityState_Response {
  type RmwMsg = super::srv::rmw::SetEntityState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetJointProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointProperties_Request {
    /// name of joint
    pub joint_name: std::string::String,

    /// access to ODE joint dynamics properties
    pub ode_joint_config: super::msg::ODEJointProperties,

}



impl Default for SetJointProperties_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetJointProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetJointProperties_Request {
  type RmwMsg = super::srv::rmw::SetJointProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name.as_str().into(),
        ode_joint_config: super::msg::ODEJointProperties::into_rmw_message(std::borrow::Cow::Owned(msg.ode_joint_config)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name.as_str().into(),
        ode_joint_config: super::msg::ODEJointProperties::into_rmw_message(std::borrow::Cow::Borrowed(&msg.ode_joint_config)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_name: msg.joint_name.to_string(),
      ode_joint_config: super::msg::ODEJointProperties::from_rmw_message(msg.ode_joint_config),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetJointProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointProperties_Response {
    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for SetJointProperties_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetJointProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetJointProperties_Response {
  type RmwMsg = super::srv::rmw::SetJointProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetJointTrajectory_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointTrajectory_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub model_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_trajectory: trajectory_msgs::msg::JointTrajectory,


    // This member is not documented.
    #[allow(missing_docs)]
    pub model_pose: geometry_msgs::msg::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub set_model_pose: bool,

    /// defaults to false
    pub disable_physics_updates: bool,

}



impl Default for SetJointTrajectory_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetJointTrajectory_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetJointTrajectory_Request {
  type RmwMsg = super::srv::rmw::SetJointTrajectory_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        joint_trajectory: trajectory_msgs::msg::JointTrajectory::into_rmw_message(std::borrow::Cow::Owned(msg.joint_trajectory)).into_owned(),
        model_pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.model_pose)).into_owned(),
        set_model_pose: msg.set_model_pose,
        disable_physics_updates: msg.disable_physics_updates,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        joint_trajectory: trajectory_msgs::msg::JointTrajectory::into_rmw_message(std::borrow::Cow::Borrowed(&msg.joint_trajectory)).into_owned(),
        model_pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.model_pose)).into_owned(),
      set_model_pose: msg.set_model_pose,
      disable_physics_updates: msg.disable_physics_updates,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model_name: msg.model_name.to_string(),
      joint_trajectory: trajectory_msgs::msg::JointTrajectory::from_rmw_message(msg.joint_trajectory),
      model_pose: geometry_msgs::msg::Pose::from_rmw_message(msg.model_pose),
      set_model_pose: msg.set_model_pose,
      disable_physics_updates: msg.disable_physics_updates,
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetJointTrajectory_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointTrajectory_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for SetJointTrajectory_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetJointTrajectory_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetJointTrajectory_Response {
  type RmwMsg = super::srv::rmw::SetJointTrajectory_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetLightProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLightProperties_Request {
    /// name of Gazebo Light
    pub light_name: std::string::String,

    /// diffuse color as red, green, blue, alpha
    pub diffuse: std_msgs::msg::ColorRGBA,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetLightProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetLightProperties_Request {
  type RmwMsg = super::srv::rmw::SetLightProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        light_name: msg.light_name.as_str().into(),
        diffuse: std_msgs::msg::ColorRGBA::into_rmw_message(std::borrow::Cow::Owned(msg.diffuse)).into_owned(),
        attenuation_constant: msg.attenuation_constant,
        attenuation_linear: msg.attenuation_linear,
        attenuation_quadratic: msg.attenuation_quadratic,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        light_name: msg.light_name.as_str().into(),
        diffuse: std_msgs::msg::ColorRGBA::into_rmw_message(std::borrow::Cow::Borrowed(&msg.diffuse)).into_owned(),
      attenuation_constant: msg.attenuation_constant,
      attenuation_linear: msg.attenuation_linear,
      attenuation_quadratic: msg.attenuation_quadratic,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      light_name: msg.light_name.to_string(),
      diffuse: std_msgs::msg::ColorRGBA::from_rmw_message(msg.diffuse),
      attenuation_constant: msg.attenuation_constant,
      attenuation_linear: msg.attenuation_linear,
      attenuation_quadratic: msg.attenuation_quadratic,
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetLightProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLightProperties_Response {
    /// return true if get successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for SetLightProperties_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetLightProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetLightProperties_Response {
  type RmwMsg = super::srv::rmw::SetLightProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetLinkProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLinkProperties_Request {
    /// name of link
    /// link names are prefixed by model name, e.g. pr2::base_link
    pub link_name: std::string::String,

    /// center of mass location in link frame
    /// and orientation of the moment of inertias
    /// relative to the link frame
    pub com: geometry_msgs::msg::Pose,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetLinkProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetLinkProperties_Request {
  type RmwMsg = super::srv::rmw::SetLinkProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
        com: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.com)).into_owned(),
        gravity_mode: msg.gravity_mode,
        mass: msg.mass,
        ixx: msg.ixx,
        ixy: msg.ixy,
        ixz: msg.ixz,
        iyy: msg.iyy,
        iyz: msg.iyz,
        izz: msg.izz,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_name: msg.link_name.as_str().into(),
        com: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.com)).into_owned(),
      gravity_mode: msg.gravity_mode,
      mass: msg.mass,
      ixx: msg.ixx,
      ixy: msg.ixy,
      ixz: msg.ixz,
      iyy: msg.iyy,
      iyz: msg.iyz,
      izz: msg.izz,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      link_name: msg.link_name.to_string(),
      com: geometry_msgs::msg::Pose::from_rmw_message(msg.com),
      gravity_mode: msg.gravity_mode,
      mass: msg.mass,
      ixx: msg.ixx,
      ixy: msg.ixy,
      ixz: msg.ixz,
      iyy: msg.iyy,
      iyz: msg.iyz,
      izz: msg.izz,
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetLinkProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLinkProperties_Response {
    /// return true if get info is successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for SetLinkProperties_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetLinkProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetLinkProperties_Response {
  type RmwMsg = super::srv::rmw::SetLinkProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetLinkState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLinkState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub link_state: super::msg::LinkState,

}



impl Default for SetLinkState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetLinkState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetLinkState_Request {
  type RmwMsg = super::srv::rmw::SetLinkState_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_state: super::msg::LinkState::into_rmw_message(std::borrow::Cow::Owned(msg.link_state)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        link_state: super::msg::LinkState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.link_state)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      link_state: super::msg::LinkState::from_rmw_message(msg.link_state),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetLinkState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLinkState_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for SetLinkState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetLinkState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetLinkState_Response {
  type RmwMsg = super::srv::rmw::SetLinkState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetModelConfiguration_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModelConfiguration_Request {
    /// model to set state
    pub model_name: std::string::String,

    /// UNUSED
    pub urdf_param_name: std::string::String,

    /// list of joints to set positions.  if joint is not listed here, preserve current position.
    pub joint_names: Vec<std::string::String>,

    /// set to this position.
    pub joint_positions: Vec<f64>,

}



impl Default for SetModelConfiguration_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetModelConfiguration_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetModelConfiguration_Request {
  type RmwMsg = super::srv::rmw::SetModelConfiguration_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        urdf_param_name: msg.urdf_param_name.as_str().into(),
        joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        joint_positions: msg.joint_positions.as_slice().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        urdf_param_name: msg.urdf_param_name.as_str().into(),
        joint_names: msg.joint_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        joint_positions: msg.joint_positions.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model_name: msg.model_name.to_string(),
      urdf_param_name: msg.urdf_param_name.to_string(),
      joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      joint_positions: msg.joint_positions.into(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetModelConfiguration_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModelConfiguration_Response {
    /// return true if setting state successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for SetModelConfiguration_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetModelConfiguration_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetModelConfiguration_Response {
  type RmwMsg = super::srv::rmw::SetModelConfiguration_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetModelState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModelState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub model_state: super::msg::ModelState,

}



impl Default for SetModelState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetModelState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetModelState_Request {
  type RmwMsg = super::srv::rmw::SetModelState_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_state: super::msg::ModelState::into_rmw_message(std::borrow::Cow::Owned(msg.model_state)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_state: super::msg::ModelState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.model_state)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model_state: super::msg::ModelState::from_rmw_message(msg.model_state),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetModelState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetModelState_Response {
    /// return true if setting state successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for SetModelState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetModelState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetModelState_Response {
  type RmwMsg = super::srv::rmw::SetModelState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetPhysicsProperties_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetPhysicsProperties_Request {
    /// dt in seconds
    pub time_step: f64,

    /// throttle maximum physics update rate
    pub max_update_rate: f64,

    /// gravity vector (e.g. earth ~[0,0,-9.81])
    pub gravity: geometry_msgs::msg::Vector3,

    /// configurations for ODE
    pub ode_config: super::msg::ODEPhysics,

}



impl Default for SetPhysicsProperties_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetPhysicsProperties_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetPhysicsProperties_Request {
  type RmwMsg = super::srv::rmw::SetPhysicsProperties_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        time_step: msg.time_step,
        max_update_rate: msg.max_update_rate,
        gravity: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Owned(msg.gravity)).into_owned(),
        ode_config: super::msg::ODEPhysics::into_rmw_message(std::borrow::Cow::Owned(msg.ode_config)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      time_step: msg.time_step,
      max_update_rate: msg.max_update_rate,
        gravity: geometry_msgs::msg::Vector3::into_rmw_message(std::borrow::Cow::Borrowed(&msg.gravity)).into_owned(),
        ode_config: super::msg::ODEPhysics::into_rmw_message(std::borrow::Cow::Borrowed(&msg.ode_config)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      time_step: msg.time_step,
      max_update_rate: msg.max_update_rate,
      gravity: geometry_msgs::msg::Vector3::from_rmw_message(msg.gravity),
      ode_config: super::msg::ODEPhysics::from_rmw_message(msg.ode_config),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SetPhysicsProperties_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetPhysicsProperties_Response {
    /// return true if set wrench successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for SetPhysicsProperties_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetPhysicsProperties_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetPhysicsProperties_Response {
  type RmwMsg = super::srv::rmw::SetPhysicsProperties_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SpawnEntity_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpawnEntity_Request {
    /// Name of the entity to be spawned (optional).
    pub name: std::string::String,

    /// Entity XML description as a string, either URDF or SDF.
    pub xml: std::string::String,

    /// Spawn robot and all ROS interfaces under this namespace
    pub robot_namespace: std::string::String,

    /// Initial entity pose.
    pub initial_pose: geometry_msgs::msg::Pose,

    /// initial_pose is defined relative to the frame of this entity.
    /// If left empty or "world" or "map", then gazebo world frame is
    /// used.
    /// If non-existent entity is specified, an error is returned
    /// and the entity is not spawned.
    pub reference_frame: std::string::String,

}



impl Default for SpawnEntity_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SpawnEntity_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SpawnEntity_Request {
  type RmwMsg = super::srv::rmw::SpawnEntity_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        xml: msg.xml.as_str().into(),
        robot_namespace: msg.robot_namespace.as_str().into(),
        initial_pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.initial_pose)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        xml: msg.xml.as_str().into(),
        robot_namespace: msg.robot_namespace.as_str().into(),
        initial_pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.initial_pose)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      xml: msg.xml.to_string(),
      robot_namespace: msg.robot_namespace.to_string(),
      initial_pose: geometry_msgs::msg::Pose::from_rmw_message(msg.initial_pose),
      reference_frame: msg.reference_frame.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SpawnEntity_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpawnEntity_Response {
    /// Return true if spawned successfully.
    pub success: bool,

    /// Comments if available.
    pub status_message: std::string::String,

}



impl Default for SpawnEntity_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SpawnEntity_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SpawnEntity_Response {
  type RmwMsg = super::srv::rmw::SpawnEntity_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SpawnModel_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpawnModel_Request {
    /// name of the model to be spawn
    pub model_name: std::string::String,

    /// this should be an urdf or gazebo xml
    pub model_xml: std::string::String,

    /// spawn robot and all ROS interfaces under this namespace
    pub robot_namespace: std::string::String,

    /// only applied to canonical body
    pub initial_pose: geometry_msgs::msg::Pose,

    /// initial_pose is defined relative to the frame of this model/body
    /// if left empty or "world", then gazebo world frame is used
    /// if non-existent model/body is specified, an error is returned
    ///   and the model is not spawned
    pub reference_frame: std::string::String,

}



impl Default for SpawnModel_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SpawnModel_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SpawnModel_Request {
  type RmwMsg = super::srv::rmw::SpawnModel_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        model_xml: msg.model_xml.as_str().into(),
        robot_namespace: msg.robot_namespace.as_str().into(),
        initial_pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.initial_pose)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
        model_xml: msg.model_xml.as_str().into(),
        robot_namespace: msg.robot_namespace.as_str().into(),
        initial_pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.initial_pose)).into_owned(),
        reference_frame: msg.reference_frame.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model_name: msg.model_name.to_string(),
      model_xml: msg.model_xml.to_string(),
      robot_namespace: msg.robot_namespace.to_string(),
      initial_pose: geometry_msgs::msg::Pose::from_rmw_message(msg.initial_pose),
      reference_frame: msg.reference_frame.to_string(),
    }
  }
}


// Corresponds to gazebo_msgs__srv__SpawnModel_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SpawnModel_Response {
    /// return true if spawn successful
    pub success: bool,

    /// comments if available
    pub status_message: std::string::String,

}



impl Default for SpawnModel_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SpawnModel_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SpawnModel_Response {
  type RmwMsg = super::srv::rmw::SpawnModel_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        status_message: msg.status_message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        status_message: msg.status_message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      status_message: msg.status_message.to_string(),
    }
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


