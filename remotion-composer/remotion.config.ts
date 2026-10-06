import path from "path";
import webpack from "webpack";
import { Config } from "@remotion/cli/config";

// Opt-in: use an existing Chrome/Chromium headless shell instead of letting
// Remotion download one (e.g. sandboxes without access to remotion.media).
if (process.env.REMOTION_BROWSER_EXECUTABLE) {
  Config.setBrowserExecutable(process.env.REMOTION_BROWSER_EXECUTABLE);
}

// Opt-in OpenGL backend for WebGL / Three.js scenes, e.g. REMOTION_GL=angle.
if (process.env.REMOTION_GL) {
  Config.setChromiumOpenGlRenderer(process.env.REMOTION_GL as "angle" | "swangle" | "egl" | "swiftshader" | "vulkan" | "angle-egl");
}

// Opt-in: render without fonts.gstatic.com. Every @remotion/google-fonts/<Font>
// import becomes a no-op stub, so locked-down networks fall back to system fonts
// instead of failing the render. Fonts shipped in public/ (e.g. fonts/yafho) are unaffected.
if (process.env.REMOTION_OFFLINE_GOOGLE_FONTS === "1") {
  const stub = path.resolve(process.cwd(), "src/offline/google-fonts-stub.ts");
  Config.overrideWebpackConfig((config) => ({
    ...config,
    plugins: [
      ...(config.plugins ?? []),
      new webpack.NormalModuleReplacementPlugin(/^@remotion\/google-fonts\/[A-Za-z0-9]+$/, (resource) => {
        const name = resource.request.split("/").pop();
        resource.request = `${stub}?${name}`;
      }),
    ],
  }));
}
