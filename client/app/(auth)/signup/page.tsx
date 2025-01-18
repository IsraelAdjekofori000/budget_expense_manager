"use client";

import React, { useState } from "react";
import apiClient from "@/utils/axios_agent";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { MdError } from "react-icons/md";

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
    nonField: "",
  });

  const router = useRouter();

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

    setErrors((error) => ({ ...error, ...newErrors }));
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
          router.push("/check-email");
        })
        .catch(function (error) {
          console.log(error);
          setErrors((errors) => ({ ...errors, nonField: error }));
        });
      console.log("Signup data:", response);
    }
  };

  return (
    <div className="w-full h-full flex justify-center items-center">
      <div className="bg-white/50 shadow-lg rounded-xl border-gray-200 border py-4 px-9 w-80 space-y-8">
        <h1 className="text-2xl font-semibold">Sign Up For Free</h1>

        {errors.nonField ? (
          <div className="my-5 bg-red-500/5 border border-l-4 border-red-500 text-red-600 rounded-md py-3 px-4 flex gap-x-4 items-start">
            <MdError className="text-red-600 text-lg" /> {errors.nonField}
          </div>
        ) : (
          ""
        )}

        <form onSubmit={handleSubmit} className="">
          <div className=" relative mt-5 ">
            <input
              type="email"
              id="email"
              name="email"
              placeholder=""
              value={formData.email}
              onChange={handleChange}
              className={`
              ${errors.email ? "border-red-500" : ""} outline-none h-11 w-full px-5 border border-gray-500 rounded-md px- bg-inherit relative peer
              `}
            />
            <label
              htmlFor="email"
              className="pointer-events-none absolute peer-placeholder-shown:top-1/2  peer-placeholder-shown:scale-90 peer-focus:top-0 top-0 peer-focus:scale-90 scale-90 -translate-y-1/2 left-5 bg-white "
            >
              Email
            </label>
          </div>
          {errors.email && <p className="text-red-500 animate-shake">{errors.email}</p>}

          <div className=" relative mt-5">
            <input
              type="password"
              id="password"
              name="password"
              placeholder=""
              value={formData.password}
              onChange={handleChange}
              className={`
              ${errors.password ? "border-red-500" : ""} outline-none h-11 w-full px-5 border border-gray-500 rounded-md px- bg-inherit relative peer
              `}
            />
            <label
              htmlFor="password"
              className="pointer-events-none absolute peer-placeholder-shown:top-1/2  peer-placeholder-shown:scale-90 peer-focus:top-0 top-0 peer-focus:scale-90 scale-90 -translate-y-1/2 left-5 bg-white "
            >
              Password
            </label>
          </div>
          {errors.password && <p className="text-red-500 ">{errors.password}</p>}

          <div className=" relative mt-5">
            <input
              type="confirmPassword"
              id="confirmPassword"
              name="confirmPassword"
              placeholder=""
              value={formData.confirmPassword}
              onChange={handleChange}
              className={`
              ${
                errors.confirmPassword ? "border-red-500" : ""
              } outline-none h-11 w-full px-5 border border-gray-500 rounded-md px- bg-inherit relative peer
              `}
            />
            <label
              htmlFor="confirmPassword"
              className="pointer-events-none absolute peer-placeholder-shown:top-1/2  peer-placeholder-shown:scale-90 peer-focus:top-0 top-0 peer-focus:scale-90 scale-90 -translate-y-1/2 left-5 bg-white "
            >
              Confirm Password
            </label>
          </div>
          {errors.confirmPassword && <p className="text-red-500 animate-shake">{errors.confirmPassword}</p>}

          <p className="text-sm">
            Already got an account?{" "}
            <Link href={"login"}>
              <span className="text-blue-500">Log in</span>{" "}
            </Link>
          </p>

          <div className="w-full flex justify-end pt-4">
            <button type="submit" className="bg-projOrange active:bg-projOrange/80 active:translate-y-px text-white shadow-md px-8 py-3 rounded-lg">
              Sign Up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default SignUp;
