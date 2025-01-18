"use client";

import React, { useEffect, useState, Suspense } from "react";
import apiClient from "@/utils/axios_agent";
import { useSearchParams } from "next/navigation";

function VerifyEmail() {
  const [verificationState, setVerificationState] = useState("Verifying Email ...");
  const param = useSearchParams();

  useEffect(() => {
    const id = param.get("id");
    if (!id) {
      setVerificationState("Invalid verification link");
      return;
    }

    apiClient
      .post(`/api/user/verify-email/?id=${id}`)
      .then((response) => {
        console.log(response);
        setVerificationState("Email Verification Successful");
      })
      .catch((error) => {
        console.log(error);
        setVerificationState("Email Verification Failed");
      });
  }, [param]);

  return (
    <section className="h-full w-full flex justify-center items-center">
      <h2>{verificationState}</h2>
    </section>
  );
}

// Wrapping VerifyEmail with Suspense
export default function VerifyEmailPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <VerifyEmail />
    </Suspense>
  );
}
