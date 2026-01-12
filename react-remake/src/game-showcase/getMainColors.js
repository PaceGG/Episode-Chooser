// Функция для получения основных цветов изображения в формате HEX
export async function getMainColors(imageUrl, colorCount = 5) {
  return new Promise((resolve) => {
    const img = new Image();
    img.crossOrigin = "Anonymous";
    img.src = imageUrl;

    img.onload = () => {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;
      const colorMap = new Map();

      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        const a = data[i + 3];

        if (a < 128) continue;

        const key = `${r},${g},${b}`;
        colorMap.set(key, (colorMap.get(key) || 0) + 1);
      }

      const rgbToHex = (r, g, b) =>
        "#" + [r, g, b].map((x) => x.toString(16).padStart(2, "0")).join("");

      const sortedColors = [...colorMap.entries()]
        .sort((a, b) => b[1] - a[1])
        .slice(0, colorCount)
        .map((entry) => {
          const [r, g, b] = entry[0].split(",").map(Number);
          return rgbToHex(r, g, b);
        });

      resolve(sortedColors);
    };

    img.onerror = () => {
      const colors = Array(colorCount).fill("#ffffff");
      resolve(colors);
    };
  });
}
