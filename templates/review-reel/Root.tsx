import { Composition } from "remotion";
import { Cover, Reel, ReelProps, calculateMetadata } from "./Composition";

// Props come from artifacts/props.json (built by `python -m lib.review_kit props`).
export const Root: React.FC = () => (
  <>
    <Composition
      id="ReviewReel"
      component={Reel}
      durationInFrames={30 * 60}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{} as ReelProps}
      calculateMetadata={calculateMetadata}
    />
    <Composition id="ReviewCover" component={Cover} durationInFrames={1} fps={30} width={1080} height={1920} defaultProps={{} as ReelProps} />
  </>
);
