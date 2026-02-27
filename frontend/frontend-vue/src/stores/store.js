import { defineStore } from 'pinia';
import axios from 'axios';

export const baseUrl = import.meta.env.VITE_BASE_URL

export const useDataStore = defineStore('data', {
    state: () => ({
        tests: [],
        belbin: [],
        belbinResult: [],
        dataBase: [],
        admins: [],
        user: null,
        isAuthenticated: false,
        authError: null,
    }),
    
    actions: {
        // Существующие методы...
        async fetchTests() {
            try {
                const response = await axios.get(`${baseUrl}/get-all-test`);
                this.tests = response.data;
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        
        async fetchBelbin() {
            try {
                const response = await axios.get(`${baseUrl}/belbin-test`, {
                    withCredentials: true,
                });
                this.belbin = response.data;
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        
        async fetchBelbinResult(result) {
            try {
                const response = await axios.post(`${baseUrl}/belbin-test`, result, {
                    withCredentials: true,
                });
                this.belbinResult = response.data;
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        
        async fetchDataBase() {
            try{
                const response = await axios.get(`${baseUrl}/get-test-results`, {
                    withCredentials: true,
                });
                this.dataBase = response.data;
            } catch (error){
                console.log('Ошибка при получении данных:', error)
                throw error;
            }
        },
        
        async fetchAdmins() {
            try{
                const response = await axios.get(`${baseUrl}/admins`, {
                    withCredentials: true,
                });
                this.admins = response.data;
            } catch (error){
                console.log('Ошибка при получении данных:', error)
                throw error;
            }
        },
        
        async fetchDeletAdmin(username) {
            try {
                const response = await axios.delete(`${baseUrl}/delete_admin`, {
                    data: { username },
                    withCredentials: true,
                });
                console.log('Ответ сервера:', response.data);
                await this.fetchAdmins();
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        
        async TransferSuperAdmin(username) {
            try {
                const response = await axios.delete(`${baseUrl}/promote-to-super-admin`, {
                    data: { username },
                    withCredentials: true,
                }); 
                console.log(response.data);
                await this.fetchAdmins();
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },

        // МЕТОДЫ ДЛЯ АВТОРИЗАЦИИ (без прямого localStorage)
        
        /**
         * Вход пользователя
         */
        async loginUser(formData) {
            this.authError = null;
            
            try {
                const response = await axios.post(`${baseUrl}/login-user`, formData, {
                    withCredentials: true,
                });
                
                if (response.data) {
                    this.user = response.data.user || response.data;
                    this.isAuthenticated = true;
                    
                    console.log('Успешный вход:', response.data);
                    return { success: true, data: response.data };
                }
            } catch (error) {
                console.error('Ошибка входа:', error);
                
                if (error.response) {
                    this.authError = error.response.data.message || 'Ошибка входа';
                } else {
                    this.authError = 'Ошибка соединения с сервером';
                }
                
                return { 
                    success: false, 
                    error: this.authError 
                };
            }
        },

        /**
         * Регистрация пользователя
         */
        async registerUser(formData) {
            this.authError = null;
            
            try {
                const response = await axios.post(`${baseUrl}/register-user`, formData, {
                    withCredentials: true,
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                
                console.log('Успешная регистрация:', response.data);
                return response.data

            } catch (error) {
                console.error('Ошибка регистрации:', error);
                
                if (error.response) {
                    if (error.response.status === 409) {
                        this.authError = 'Пользователь с таким Telegram уже существует';
                    } else {
                        this.authError = error.response.data.message || 'Ошибка регистрации';
                    }
                } else {
                    this.authError = 'Ошибка соединения с сервером';
                }
                
                return { 
                    success: false, 
                    error: this.authError 
                };
            }
        },

        /**
         * Выход пользователя
         */
        async logoutUser() {
            try {
                // Если есть эндпоинт для выхода
                // await axios.post(`${baseUrl}/api/logout`, {}, {
                //     withCredentials: true,
                // });
                
                // Просто очищаем состояние, persist сам обновит localStorage
                this.user = null;
                this.isAuthenticated = false;
                this.authError = null;
                
                console.log('Выход выполнен');
            } catch (error) {
                console.error('Ошибка при выходе:', error);
            }
        },

        /**
         * Проверка авторизации при загрузке приложения
         * Теперь просто проверяем, есть ли данные в state (persist уже восстановил их)
         */
        checkAuth() {
            // persist уже восстановил состояние из localStorage
            // Просто логируем для отладки
            if (this.isAuthenticated) {
                console.log('Пользователь авторизован:', this.user);
            } else {
                console.log('Пользователь не авторизован');
            }
        },

        /**
         * Обновление данных пользователя
         */
        updateUserData(userData) {
            this.user = { ...this.user, ...userData };
            // persist сам сохранит изменения
        },

        /**
         * Очистка ошибок авторизации
         */
        clearAuthError() {
            this.authError = null;
        }
    },

    getters: {
        // Существующие геттеры...
        getTests: (state) => state.tests,
        getBelbin: (state) => state.belbin,
        getBelbinResult: (state) => state.belbinResult,
        getDataBase: (state) => state.dataBase,
        getAdmins: (state) => state.admins,
        
        // Геттеры авторизации
        getUser: (state) => state.user,
        getIsAuthenticated: (state) => state.isAuthenticated,
        getAuthError: (state) => state.authError,
        
        getIsAdmin: (state) => {
            return state.user?.role === 'admin' || state.user?.role === 'super_admin';
        },
        
        getIsSuperAdmin: (state) => state.user?.role === 'super_admin',
        
        getUserName: (state) => {
            if (!state.user) return '';
            return state.user.full_name || state.user.username || 'Пользователь';
        },
    },
    
    persist: {
        key: 'data-store',
        storage: window.localStorage,
        // persist сам позаботится о сохранении и восстановлении этих полей
        paths: ['tests', 'belbin', 'belbinResult', 'user', 'isAuthenticated'],
    },
});