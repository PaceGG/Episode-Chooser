// oauth.js
const CLIENT_ID = 'ваш_client_id.apps.googleusercontent.com';
const API_KEY = 'AIzaSyA5ErlvPrDU-QskKoYkyY60Ah5OyePHnwo';
const SCOPES = 'https://www.googleapis.com/auth/youtube.readonly';

export async function authorize() {
    return new Promise((resolve, reject) => {
        window.gapi.load('client:auth2', () => {
            window.gapi.client.init({
                apiKey: API_KEY,
                clientId: CLIENT_ID,
                scope: SCOPES,
                discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest']
            }).then(() => {
                const auth = window.gapi.auth2.getAuthInstance();
                
                // Проверяем, есть ли сохраненный токен
                const savedToken = localStorage.getItem('youtube_token');
                
                if (auth.isSignedIn.get()) {
                    // Уже авторизован
                    console.log('Уже авторизован');
                    resolve();
                } else if (savedToken) {
                    // Пытаемся восстановить сессию
                    auth.signIn({
                        prompt: 'none'
                    }).then(() => {
                        console.log('Сессия восстановлена');
                        resolve();
                    }).catch(() => {
                        // Если не удалось восстановить, запрашиваем авторизацию
                        auth.signIn().then(resolve).catch(reject);
                    });
                } else {
                    // Запрашиваем авторизацию
                    auth.signIn().then(() => {
                        // Сохраняем токен
                        const currentUser = auth.currentUser.get();
                        const token = currentUser.getAuthResponse().access_token;
                        localStorage.setItem('youtube_token', token);
                        localStorage.setItem('youtube_token_expiry', String(Date.now() + 3600000));
                        resolve();
                    }).catch(reject);
                }
            }).catch(reject);
        });
    });
}

export function getAuthHeaders() {
    const auth = window.gapi.auth2.getAuthInstance();
    const currentUser = auth.currentUser.get();
    const token = currentUser.getAuthResponse().access_token;
    
    // Обновляем токен в localStorage при каждом запросе
    localStorage.setItem('youtube_token', token);
    localStorage.setItem('youtube_token_expiry', String(Date.now() + 3600000));
    
    return {
        'Authorization': `Bearer ${token}`
    };
}

// Функция для проверки и обновления токена
export function isTokenValid() {
    const expiry = localStorage.getItem('youtube_token_expiry');
    if (!expiry) return false;
    
    const now = Date.now();
    const expiryTime = parseInt(expiry, 10);
    
    // Токен действителен еще 5 минут
    return now < expiryTime - 300000;
}

// Выход из аккаунта
export function signOut() {
    const auth = window.gapi.auth2.getAuthInstance();
    auth.signOut().then(() => {
        localStorage.removeItem('youtube_token');
        localStorage.removeItem('youtube_token_expiry');
        console.log('Выход выполнен');
    });
}