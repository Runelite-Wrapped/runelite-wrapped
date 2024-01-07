"use client";

import Link from "next/link";

export default function Navbar() {
    return(
        <div className="w-full m-0 p-0">
            <div className="bg-osrslb-150 w-full text-osrs">
                <p className="text-osrslb-700 text-3xl font-extralight pl-4 pb-1 pt-4 m-0">
                    <Link
                    href="/"
                    >
                        RuneLite<strong> Wrapped</strong>
                    </Link>
                </p>
            </div>
            <div className="h-[1px] bg-osrslb-200"></div>
        </div>
    )
}