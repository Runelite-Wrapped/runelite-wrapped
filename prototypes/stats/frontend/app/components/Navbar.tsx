"use client";

import Link from "next/link";

export default function Navbar() {
    return(
        <div className="w-full h-1/6 m-0 p-0">
            <div className="bg-osrslb-150 h-full">
                <div className="flex mx-auto w-4/6 text-osrs h-full">
                    <p className="text-osrslb-700 text-6xl font-extralight pl-4 mb-4 pt-4 mx-0 mt-auto align-middle">
                        <Link
                        href="/"
                        >
                            RuneLite<strong> Wrapped</strong>
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}