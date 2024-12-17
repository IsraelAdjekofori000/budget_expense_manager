"use client";

import Image from "next/image";
import React, { useEffect, useState } from "react";

function TypeStyle({
  tag,
  className,
  text,
  reverseEffect,
  delay,
}: {
  text: string;
  className: string;
  tag: string;
  reverseEffect?: boolean;
  delay?: number;
}) {
  const [endOfBufferPointer, setEndOfBufferPointer] = useState(0);
  const [step, setStep] = useState(1);

  useEffect(() => {
    if (endOfBufferPointer > 0) {
      if (endOfBufferPointer < text.length) setTimeout(() => setEndOfBufferPointer((iter) => iter + step), 80);
      else if (endOfBufferPointer === text.length && reverseEffect) {
        setTimeout(() => {
          setStep(-1);
          setEndOfBufferPointer((iter) => iter - 1);
        }, delay || 1000);
      }
      // console.log("here", endOfBufferPointer, text.length);
    }
  }, [text.length, endOfBufferPointer, step, reverseEffect, delay]);

  useEffect(() => {
    setEndOfBufferPointer(1);
  }, []);

  return React.createElement(
    tag,
    { className: `${className} after:content-['|'] after:font-normal after:animate-blink` },
    <>{text.slice(0, endOfBufferPointer)}</>
  );
}

export default function Home() {
  const [index, setI] = useState(1);
  // setTimeout(() => {
  //   setI((p) => p +30 + index);
  // }, 1000);

  return (
    <div className="h-full w-full pt-14 relative">
      <div className="mx-auto  w-fit">
        <div className="w-[80vw] h-[450px] overflow-hidden relative">
          {/* <Image
            src={"/coming-soon.svg"}
            alt={"Coming soon img"}
            width={400}
            height={400}
            className="rotate-[-60deg] blur-[1px] -translate-x-[100px] translate-y-[300px] absolute left1/2 -translate-x1/2"
          /> */}
          <Image
            src={"/coming-soon.svg"}
            alt={"Coming soon img"}
            width={400}
            height={400}
            className={`rotate-[${10 + 10}deg] absolute left-1/2 -translate-x-1/2`}
          />
          {/* <Image src={"/coming-soon.svg"} alt={"Coming soon img"} width={400} height={400} className=" absolute left-1/2 -translate-x-1/2" /> */}
        </div>

        <TypeStyle tag="h2" className={`font-bold text-[49px] text-center `} text="Coming Soon" reverseEffect={true} delay={7000} />
      </div>
    </div>
  );
}
