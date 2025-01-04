"use client";

import React, { useState } from "react";
import apiClient from "@/utils/axios_agent";

function SignUp() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [errors, setErrors] = useState({
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const validateForm = () => {
    let isValid = true;
    const newErrors = { email: "", password: "", confirmPassword: "" };

    if (!formData.email) {
      isValid = false;
      newErrors.email = "Email is required.";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      isValid = false;
      newErrors.email = "Invalid email format.";
    }

    if (!formData.password) {
      isValid = false;
      newErrors.password = "Password is required.";
    } else if (formData.password.length < 6) {
      isValid = false;
      newErrors.password = "Password must be at least 6 characters long.";
    }

    if (formData.password !== formData.confirmPassword) {
      isValid = false;
      newErrors.confirmPassword = "Passwords do not match.";
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (validateForm()) {
      alert("Form submitted successfully!");
      const response = apiClient
        .post("/api/user/register/user/", formData)
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
      console.log("Signup data:", response);
    }
  };

  return (
    <div className="w-full h-full flex justify-center items-center">
      <div className="bg-white rounded-xl border-gray-200 border py-4 px-11 w-80">
        <h1 className="text-2xl font-semibold">Sign Up For Free</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email">Email:</label>
            <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} />
            {errors.email && <p className="error">{errors.email}</p>}
          </div>
          <div>
            <label htmlFor="password">Password:</label>
            <input type="password" id="password" name="password" value={formData.password} onChange={handleChange} />
            {errors.password && <p className="error">{errors.password}</p>}
          </div>
          <div>
            <label htmlFor="confirmPassword">Confirm Password:</label>
            <input type="password" id="confirmPassword" name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} />
            {errors.confirmPassword && <p className="error">{errors.confirmPassword}</p>}
          </div>
          <button type="submit">Sign Up</button>
        </form>
      </div>
    </div>
  );
}

export default SignUp;
