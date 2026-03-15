const { contextBridge, ipcRenderer } = require('electron');

// Экспортируем защищенные API в рендерер процесс
contextBridge.exposeInMainWorld('electronAPI', {
    // Отправка сообщений в main процесс
    sendToMain: (channel, data) => {
        const validChannels = ['to-backend'];
        if (validChannels.includes(channel)) {
            ipcRenderer.send(channel, data);
        }
    },
    
    // Получение сообщений из main процесса
    onFromMain: (channel, func) => {
        const validChannels = ['from-backend'];
        if (validChannels.includes(channel)) {
            ipcRenderer.on(channel, (event, ...args) => func(...args));
        }
    },
    
    // Удаление слушателей
    removeListeners: (channel) => {
        ipcRenderer.removeAllListeners(channel);
    }
});

console.log('Preload script loaded successfully');