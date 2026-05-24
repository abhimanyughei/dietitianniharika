import React from "react";

// Simple Tina UI component to preview a YouTube video URL in the editor.
// Usage: set `ui: { component: 'YouTubePreview' }` on a string field that stores the video URL.

const toEmbed = (url) => {
  if (!url) return null;
  if (url.includes("watch?v=")) return url.replace("watch?v=", "embed/");
  if (url.includes("youtu.be/")) return url.replace("youtu.be/", "www.youtube.com/embed/");
  return url;
};

export default function YouTubePreview({ input }) {
  const url = input.value || "";
  const embed = toEmbed(url);
  return (
    <div>
      <input {...input} placeholder='YouTube URL' style={{ width: "100%", padding: "8px", marginBottom: "8px" }} />
      {embed ? (
        <div style={{ position: "relative", paddingBottom: "56.25%", height: 0 }}>
          <iframe
            src={embed}
            title='YouTube preview'
            style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%" }}
            frameBorder='0'
            allowFullScreen
          />
        </div>
      ) : (
        <div style={{ color: "#666", fontSize: 13 }}>Enter a YouTube URL to preview.</div>
      )}
    </div>
  );
}
