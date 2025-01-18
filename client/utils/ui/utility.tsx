import React from "react";
import { useEffect, useState } from "react";

export function TypeStyle({
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
