// sbe/src/types/vanta.d.ts

// Strongly-typed specific file:
declare module "vanta/dist/vanta.globe.min.js" {
  interface VantaEffect {
    destroy(): void;
  }
  const VANTA: (options: any) => VantaEffect;
  export default VANTA;
}

// (optional) catch-all for other Vanta effects if you use them later
declare module "vanta/dist/*" {
  const VANTA: any;
  export default VANTA;
}
