"use client";

import React from "react";
import Image from "next/image";
import { TypeStyle } from "@/utils/ui/utility";

function CheckEmail() {
  return (
    <div className="h-full w-full flex  justify-center items-center">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full  h-1/2">
        <Image src="/check-email.jpg" fill={true} alt="check-email" className="opacity-10 -z-10 object-cover" />
      </div>

      <div className="h-96 w-5/6 rounded-2xl p-4 relative">
        <TypeStyle text={"Check Inbox !!!"} className={"font-bold text-3xl  text-gray-700"} tag={"h2"}></TypeStyle>

        <div className="absolute bottom-0">
          <p className="mt-16 text-sm">We&apos;ve sent a verification email to your inbox. </p>

          <p className="mt-3 text-sm">
            <span className="font-bold">Didn&apos;t receive the email?</span> <span className="text-blue-500">Resend</span>
          </p>
        </div>
      </div>
    </div>
  );
}

export default CheckEmail;
