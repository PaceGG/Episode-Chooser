const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let backendProcess;

function startBackend() {
    // Путь к Python скрипту
    const backendPath = path.join(__dirname, 'backend', 'api.py');
    
    // Проверяем существование файла
    if (!fs.existsSync(backendPath)) {
        console.error('Backend file not found:', backendPath);
        return;
    }
    
    // Определяем Python команду
    const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';
    
    console.log('Starting backend:', pythonCommand, backendPath);
    
    // Запускаем backend
    backendProcess = spawn(pythonCommand, [backendPath]);
    
    backendProcess.stdout.on('data', (data) => {
        console.log(`Backend stdout: ${data}`);
    });
    
    backendProcess.stderr.on('data', (data) => {
        console.error(`Backend stderr: ${data}`);
    });
    
    backendProcess.on('error', (error) => {
        console.error('Failed to start backend:', error);
    });
    
    backendProcess.on('close', (code) => {
        console.log(`Backend process exited with code ${code}`);
    });
}

function createWindow() {
    // Создаем окно браузера
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: false, // Временно отключаем для разработки
            preload: path.join(__dirname, 'preload.js')
        }
    });

    // В development режиме
    if (process.env.NODE_ENV === 'development') {
        // Загружаем с сервера разработки Vite
        mainWindow.loadURL('http://localhost:5173');
        mainWindow.webContents.openDevTools();
    } else {
        // В production - ИСПРАВЛЕНО: используем файловый протокол правильно
        const frontendPath = path.join(__dirname, 'frontend', 'dist', 'index.html');
        
        // Проверяем существование файла
        if (fs.existsSync(frontendPath)) {
            console.log('Loading frontend from:', frontendPath);
            mainWindow.loadFile(frontendPath);
        } else {
            console.error('Frontend build not found at:', frontendPath);
            // Запасной вариант - показать сообщение об ошибке
            mainWindow.loadURL('data:text/html;charset=utf-8,' + 
                encodeURIComponent('<h1>Error: Frontend build not found</h1>'));
        }
    }

    // Обработка закрытия окна
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// Этот метод будет вызван когда Electron завершит инициализацию
app.whenReady().then(() => {
    startBackend();
    createWindow();
});

// Выход когда все окна закрыты
app.on('window-all-closed', () => {
    if (backendProcess) {
        backendProcess.kill();
    }
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// Обработка IPC сообщений от рендерера
ipcMain.on('to-backend', (event, data) => {
    console.log('Message from renderer:', data);
    // Здесь можно отправить данные в backend процесс
});

// Дополнительная обработка ошибок
process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
});