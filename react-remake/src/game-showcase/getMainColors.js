// Функция для получения основных цветов изображения
export async function getMainColors(imageUrl, colorCount = 5) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = "Anonymous"; // важно для кроссдоменных изображений
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

      // Проходим по всем пикселям
      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        const a = data[i + 3];

        // Игнорируем прозрачные пиксели
        if (a < 128) continue;

        const key = `${r},${g},${b}`;
        colorMap.set(key, (colorMap.get(key) || 0) + 1);
      }

      // Сортируем цвета по количеству
      const sortedColors = [...colorMap.entries()]
        .sort((a, b) => b[1] - a[1])
        .slice(0, colorCount)
        .map((entry) => `rgb(${entry[0]})`);

      resolve(sortedColors);
    };

    img.onerror = () => {
      const colors = Array(colorCount).fill("rgb(255,255,255)");
      return colors;
    };
  });
}
