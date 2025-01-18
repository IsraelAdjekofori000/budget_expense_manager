"use client";

import Image from "next/image";
import { TypeStyle } from "@/utils/ui/utility";

export default function Home() {
  // const [index, setI] = useState(1);
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
