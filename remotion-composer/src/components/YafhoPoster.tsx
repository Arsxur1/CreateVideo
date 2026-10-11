import React from "react";
import { AbsoluteFill, Img, staticFile, useVideoConfig } from "remotion";
import { YAFHO, useYafhoFonts } from "./yafho/tokens";

/**
 * Yafho-Silicare science posters (A4 print and Instagram 4:5) — «зачем пластина и насколько помогает».
 * One still per variant; all text and the QR come from code, illustrations are the same 3D
 * cross-sections and skin textures the videos use. Facts: product passport (TZ §0) and the
 * study table (TZ §0.1) only, every figure with its source line.
 */
export type PosterVariant = "why" | "how" | "howmuch" | "care";

export type YafhoPosterProps = {
  variant: PosterVariant;
  /** public-relative image paths rendered by make_posters.py */
  images?: { alarm?: string; seal?: string; hyper?: string; soft?: string };
  qr?: number[][];
  page?: string;
};

const SOURCE_HSU = "Hsu K-C, Luan C-W, Tsai Y-W. Wounds 2017;29(5):154–158";
const SOURCE_MONSTREY = "Monstrey S. et al. Updated Scar Management Practical Guidelines. J Plast Reconstr Aesthet Surg, 2014";
const DISCLAIMER = "Информация не заменяет консультацию врача. Не используйте на открытой ране. Дети, беременность — сначала к врачу.";

const TITLES: Record<PosterVariant, { kicker: string; title: string; lead: string }> = {
  why: {
    kicker: "Наука простыми словами · 1 / 4",
    title: "Почему рубец\nрастёт",
    lead: "Рана зажила, а рубец становится плотнее и заметнее. Так кожа реагирует на потерю влаги.",
  },
  how: {
    kicker: "Наука простыми словами · 2 / 4",
    title: "Как работает\nсиликон",
    lead: "Пластина из медицинского силикона держит влагу в рубце — и кожа успокаивается.",
  },
  howmuch: {
    kicker: "Наука простыми словами · 3 / 4",
    title: "Насколько это\nпомогает",
    lead: "Что говорят исследования и когда ждать изменений.",
  },
  care: {
    kicker: "Памятка пациенту · 4 / 4",
    title: "Уход за рубцом\nс пластиной",
    lead: "Всё, что нужно знать дома: когда начинать, как носить, чего ждать и когда нельзя.",
  },
};

export const YafhoPoster: React.FC<YafhoPosterProps> = ({ variant, images = {}, qr, page }) => {
  useYafhoFonts();
  const { width, height } = useVideoConfig();
  const u = width / 1080; // design unit: layouts are drawn for 1080 px wide
  const tall = height / width > 1.35; // A4 has room for more air than 4:5
  const t = TITLES[variant];
  const pad = 72 * u;

  const text = (size: number, weight = 500, color: string = YAFHO.navy): React.CSSProperties => ({
    fontFamily: YAFHO.sans,
    fontSize: size * u,
    fontWeight: weight,
    color,
    lineHeight: 1.22,
    margin: 0,
  });

  return (
    <AbsoluteFill style={{ background: YAFHO.offWhite, padding: pad, display: "flex", flexDirection: "column", gap: (tall ? 34 : 22) * u }}>
      {/* header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <p style={text(26, 800)}>
          Yafho<span style={{ fontWeight: 500 }}>-Silicare</span>
        </p>
        <p style={{ ...text(22, 700, YAFHO.tealText), fontFamily: YAFHO.mono }}>{t.kicker}</p>
      </div>
      <div style={{ width: 96 * u, height: 8 * u, background: YAFHO.orange, borderRadius: 4 * u }} />
      <h1 style={{ ...text(tall ? 92 : 76, 800), whiteSpace: "pre-line", lineHeight: 1.04 }}>{t.title}</h1>
      {tall && <p style={{ ...text(34, 500, YAFHO.navy), maxWidth: 900 * u }}>{t.lead}</p>}

      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: (tall ? 30 : 20) * u, minHeight: 0 }}>
        {variant === "why" && <Why u={u} tall={tall} text={text} images={images} />}
        {variant === "how" && <How u={u} tall={tall} text={text} images={images} />}
        {variant === "howmuch" && <HowMuch u={u} tall={tall} text={text} />}
        {variant === "care" && <Care u={u} tall={tall} text={text} />}
      </div>

      {/* footer */}
      <div style={{ display: "flex", alignItems: "flex-end", gap: 28 * u, borderTop: `${2 * u}px solid ${YAFHO.beige}`, paddingTop: 20 * u }}>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 8 * u }}>
          <p style={text(19, 500, YAFHO.muted)}>{DISCLAIMER}</p>
          <p style={text(22, 800)}>
            @sil.icare {page ? <span style={{ fontWeight: 500, color: YAFHO.muted }}> · {page}</span> : null}
          </p>
        </div>
        {qr && qr.length > 0 && <Qr qr={qr} size={(variant === "care" ? 168 : 132) * u} />}
      </div>
    </AbsoluteFill>
  );
};

type TextFn = (size: number, weight?: number, color?: string) => React.CSSProperties;
type Part = { u: number; tall: boolean; text: TextFn; images?: YafhoPosterProps["images"] };

const Qr: React.FC<{ qr: number[][]; size: number }> = ({ qr, size }) => (
  <div style={{ background: YAFHO.white, padding: size * 0.07, borderRadius: size * 0.08, border: `2px solid ${YAFHO.beige}` }}>
    <svg width={size} height={size} viewBox={`0 0 ${qr.length} ${qr.length}`} shapeRendering="crispEdges">
      {qr.flatMap((row, y) => row.map((v, x) => (v ? <rect key={`${x}-${y}`} x={x} y={y} width={1} height={1} fill={YAFHO.navy} /> : null)))}
    </svg>
  </div>
);

/** Rounded picture (3D cross-section or skin close-up) with an optional small tag. */
const Picture: React.FC<{ src?: string; u: number; h: number; tag?: string; fit?: "cover" | "contain"; scale?: number; grow?: boolean }> = ({
  src,
  u,
  h,
  tag,
  fit = "cover",
  scale = 1,
  grow = false,
}) => (
  <div style={{ position: "relative", ...(grow ? { flex: "1 1 0", minHeight: h } : { flex: "none", height: h }), borderRadius: 28 * u, overflow: "hidden", background: YAFHO.white, boxShadow: `0 ${6 * u}px ${24 * u}px rgba(15,36,64,0.10)` }}>
    {src && (
      <Img
        src={staticFile(src)}
        style={{ width: "100%", height: "100%", objectFit: fit, transform: `scale(${scale})`, transformOrigin: "50% 50%" }}
      />
    )}
    {tag && (
      <span
        style={{
          position: "absolute",
          right: 16 * u,
          bottom: 14 * u,
          background: "rgba(255,255,255,0.92)",
          color: YAFHO.muted,
          fontFamily: YAFHO.sans,
          fontSize: 17 * u,
          fontWeight: 600,
          padding: `${4 * u}px ${10 * u}px`,
          borderRadius: 8 * u,
        }}
      >
        {tag}
      </span>
    )}
  </div>
);

/** Numbered step: a navy disc with the number and two lines of text. */
const Step: React.FC<{ n: string; head: string; body?: string; u: number; text: TextFn; color?: string }> = ({ n, head, body, u, text, color = YAFHO.navy }) => (
  <div style={{ display: "flex", gap: 22 * u, alignItems: "flex-start" }}>
    <div
      style={{
        flex: "none",
        width: 56 * u,
        height: 56 * u,
        borderRadius: "50%",
        background: color,
        color: YAFHO.white,
        fontFamily: YAFHO.mono,
        fontWeight: 700,
        fontSize: 28 * u,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      {n}
    </div>
    <div style={{ display: "flex", flexDirection: "column", gap: 4 * u, paddingTop: 6 * u }}>
      <p style={text(33, 800)}>{head}</p>
      {body && <p style={text(25, 500, YAFHO.muted)}>{body}</p>}
    </div>
  </div>
);

/** Figure + label + source, the poster version of the video stat badge. */
const Figure: React.FC<{ value: string; label: string; source: string; u: number; text: TextFn; big?: boolean; compact?: boolean }> = ({ value, label, source, u, text, big, compact }) => (
  <div style={{ flex: "1 1 0", minWidth: 0, background: YAFHO.white, borderRadius: 24 * u, borderTop: `${8 * u}px solid ${YAFHO.teal}`, padding: `${22 * u}px ${26 * u}px`, display: "flex", flexDirection: "column", gap: 8 * u }}>
    <p style={{ ...text(big ? (compact ? 78 : 96) : compact ? 52 : 64, 800), fontFamily: YAFHO.sans, letterSpacing: -1 * u, lineHeight: 1 }}>{value}</p>
    <p style={{ ...text(big && !compact ? 30 : 25, 700), whiteSpace: "pre-line" }}>{label}</p>
    <p style={text(16, 500, YAFHO.muted)}>{source}</p>
  </div>
);

const Why: React.FC<Part> = ({ u, tall, text, images }) => (
  <>
    <Picture src={images?.alarm} u={u} h={220 * u} tag="схема" grow />
    <div style={{ flex: "none", display: "flex", flexDirection: "column", gap: (tall ? 22 : 12) * u }}>
      <Step n="1" head="Молодой рубец теряет влагу" u={u} text={text} />
      <Step n="2" head="Кожа «бьёт тревогу»" body="фибробласты получают сигнал строить коллаген" u={u} text={text} />
      <Step n="3" head="Лишний коллаген" body="рубец становится плотным и заметным" u={u} text={text} color={YAFHO.orangeText} />
    </div>
    <div style={{ flex: "none", display: "flex", gap: 20 * u }}>
      <Figure value="39–68 %" label={"гипертрофический рубец\nпосле операций"} source={SOURCE_HSU} u={u} text={text} />
      <Figure value="33–91 %" label={"гипертрофический рубец\nпосле ожогов"} source={SOURCE_HSU} u={u} text={text} />
    </div>
  </>
);

const How: React.FC<Part> = ({ u, tall, text, images }) => (
  <>
    <Picture src={images?.seal} u={u} h={180 * u} tag="схема" grow />
    <div style={{ flex: "none", display: "flex", flexDirection: "column", gap: (tall ? 20 : 8) * u }}>
      <Step n="1" head="Пластина держит влагу в коже" body="окклюзия: вода не уходит из рубца" u={u} text={text} color={YAFHO.tealText} />
      <Step n="2" head="Сигнал тревоги слабее" body="фибробласты получают сигнал реже" u={u} text={text} color={YAFHO.tealText} />
      <Step n="3" head="Меньше лишнего коллагена" body="волокна ложатся ровнее" u={u} text={text} color={YAFHO.tealText} />
      <Step n="✓" head="Кислород проходит" u={u} text={text} color={YAFHO.tealText} />
    </div>
    <div style={{ flex: "none", display: "flex", gap: 20 * u, alignItems: "stretch" }}>
      {(
        [
          ["Без ухода", images?.hyper, YAFHO.orangeText],
          ["С силиконом", images?.soft, YAFHO.tealText],
        ] as const
      ).map(([label, src, color]) => (
        <div key={label} style={{ flex: 1, display: "flex", flexDirection: "column", gap: 10 * u }}>
          <p style={text(24, 800, color)}>● {label}</p>
          <Picture src={src} u={u} h={(tall ? 220 : 112) * u} scale={1.9} tag="схема" />
        </div>
      ))}
    </div>
    <p style={{ ...text(tall ? 40 : 32, 800), textAlign: "center", flex: "none" }}>Рубец мягче, площе, светлее</p>
  </>
);

const HowMuch: React.FC<Part> = ({ u, tall, text }) => (
  <>
    <div style={{ flex: "none" }}><Figure value="≈ в 2 раза" label={"ниже риск патологического рубца\nс силиконовыми пластинами"} source={`${SOURCE_HSU} · RR 0,41`} u={u} text={text} big compact={!tall} /></div>
    <div style={{ flex: "none" }}><Figure value="1-я линия" label={"«золотой стандарт» неинвазивной\nтерапии рубцов"} source={SOURCE_MONSTREY} u={u} text={text} compact={!tall} /></div>
    <div style={{ flex: "none", background: YAFHO.white, borderRadius: 24 * u, padding: `${(tall ? 30 : 18) * u}px ${28 * u}px`, display: "flex", flexDirection: "column", gap: (tall ? 18 : 10) * u }}>
      <p style={text(30, 800)}>Когда ждать изменений</p>
      <div style={{ position: "relative", height: 10 * u, borderRadius: 5 * u, background: YAFHO.beige }}>
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: "100%", borderRadius: 5 * u, background: YAFHO.teal }} />
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 16 * u }}>
        {[
          ["недели", "первые изменения"],
          ["1–3 мес", "заметно"],
          ["3–6 мес", "ровнее"],
        ].map(([when, what]) => (
          <div key={when} style={{ flex: 1, display: "flex", flexDirection: "column", gap: 4 * u }}>
            <p style={{ ...text(34, 800, YAFHO.tealText), fontFamily: YAFHO.mono }}>{when}</p>
            <p style={text(25, 600)}>{what}</p>
          </div>
        ))}
      </div>
      <p style={text(21, 500, YAFHO.muted)}>при регулярном ношении — схема по срокам из инструкции</p>
    </div>
    <div style={{ flex: "none", borderLeft: `${6 * u}px solid ${YAFHO.orange}`, paddingLeft: 22 * u, display: "flex", flexDirection: "column", gap: 6 * u }}>
      <p style={text(26, 800)}>Честно о доказательствах</p>
      <p style={text(tall ? 23 : 21, 500)}>
        Качество многих исследований низкое (Cochrane CD003826). Поэтому мы говорим «снижает риск» и «помогает» — рубец
        становится мягче, светлее, ровнее.
      </p>
    </div>
  </>
);

const Block: React.FC<{ title: string; u: number; text: TextFn; accent: string; children: React.ReactNode }> = ({ title, u, text, accent, children }) => (
  <div style={{ background: YAFHO.white, borderRadius: 22 * u, borderLeft: `${8 * u}px solid ${accent}`, padding: `${18 * u}px ${24 * u}px`, display: "flex", flexDirection: "column", gap: 8 * u }}>
    <p style={text(27, 800)}>{title}</p>
    {children}
  </div>
);

const Line: React.FC<{ mark: string; color: string; u: number; text: TextFn; children: React.ReactNode }> = ({ mark, color, u, text, children }) => (
  <div style={{ display: "flex", gap: 14 * u, alignItems: "baseline" }}>
    <span style={{ ...text(24, 800, color), fontFamily: YAFHO.mono, minWidth: 30 * u }}>{mark}</span>
    <p style={text(24, 500)}>{children}</p>
  </div>
);

const Care: React.FC<Part> = ({ u, tall, text }) => (
  <div style={{ display: "flex", flexDirection: "column", gap: (tall ? 22 : 14) * u }}>
    <Block title="Когда начинать" u={u} text={text} accent={YAFHO.teal}>
      <Line mark="✓" color={YAFHO.tealText} u={u} text={text}>сразу после закрытия раны и снятия швов</Line>
      <Line mark="✓" color={YAFHO.tealText} u={u} text={text}>нет корок и воспаления</Line>
    </Block>
    <Block title="Как носить" u={u} text={text} accent={YAFHO.navy}>
      <Line mark="1" color={YAFHO.navy} u={u} text={text}>очистить и высушить кожу</Line>
      <Line mark="2" color={YAFHO.navy} u={u} text={text}>пластина на 1 см шире рубца со всех сторон</Line>
      <Line mark="3" color={YAFHO.navy} u={u} text={text}>носить 12–23 ч в сутки</Line>
      <Line mark="4" color={YAFHO.navy} u={u} text={text}>промывать, чередовать две пластины</Line>
    </Block>
    <Block title="Чего ждать" u={u} text={text} accent={YAFHO.teal}>
      <Line mark="→" color={YAFHO.tealText} u={u} text={text}>недели — первые изменения</Line>
      <Line mark="→" color={YAFHO.tealText} u={u} text={text}>1–3 мес — заметно, 3–6 мес — ровнее</Line>
    </Block>
    <Block title="Нельзя" u={u} text={text} accent={YAFHO.orange}>
      <Line mark="✗" color={YAFHO.orangeText} u={u} text={text}>открытая рана, корки, инфекция, аллергия на силикон</Line>
      <Line mark="!" color={YAFHO.orangeText} u={u} text={text}>дети, беременность — сначала к врачу</Line>
    </Block>
  </div>
);
