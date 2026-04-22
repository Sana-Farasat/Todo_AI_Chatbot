// import type { NextConfig } from "next";

// const nextConfig: NextConfig = {
//   /* config options here */
// };

// export default nextConfig;

// next.config.mjs

/** @type {import('next').NextConfig} */
const nextConfig = {

   experimental: {
    turbopack: false,
  },
  webpack: (config) => {
    config.resolve.fallback = {
      dns: false,
      net: false,
      tls: false,
      pg: false,
    };
    
    return config;
  },
};

export default nextConfig;