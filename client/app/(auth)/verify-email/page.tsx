"use client";

import React, { useEffect, useState } from "react";
import apiClient from "@/utils/axios_agent";
import { useSearchParams } from "next/navigation";

function VerifyEmail() {
  const [verificationState, useVerificationState] = useState("Verifying Email ...");
  const param = useSearchParams();

  
  useEffect(() => {
    const response = apiClient
      .post(`/api/user/verify-email/?id=${param.get("id")}`)
      .then((response) => {
        console.log(response);
        useVerificationState('Email Verification Successfull')
      })
      .catch((error) => {
        console.log(error);
      });
    
  }, []);
  
  return (
    <section className="h-full w-full flex justify-center items-center">
      <h2 className="">{verificationState}</h2>
    </section>
  );
}

export default VerifyEmail;
