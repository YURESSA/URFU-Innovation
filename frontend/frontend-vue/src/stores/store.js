import { defineStore } from 'pinia';
import axios from 'axios';

export const baseUrl = import.meta.env.VITE_BASE_URL

export const useDataStore = defineStore('data', {
    state: () => ({
        tests: [],
        belbin: [],
        disc: [],
        belbinResult: [],
        discResult: [],
        dataBase: [],
        admins: [],
        userTest: null,
        user: null,
        isAuthenticated: false,
        authError: null,
    }),
    
    actions: {
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

        async fetchDisc() {
            try {
                const response = await axios.get(`${baseUrl}/disc-test`, {
                    withCredentials: true,
                });
                this.disc = response.data;
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
        
        async fetchDiscResult(result) {
            try {
                const response = await axios.post(`${baseUrl}/disc-test`, result, {
                    withCredentials: true,
                });
                this.discResult = response.data;
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

        async loginUser(formData) {
            this.authError = null;
            
            try {
                const response = await axios.post(`${baseUrl}/login-user`, formData, {
                    withCredentials: true,
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
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

        async logoutUser() {
            try {
                await axios.post(`${baseUrl}/logout-user`, {}, {
                    withCredentials: true,
                });
                
                this.user = null;
                this.isAuthenticated = false;
                this.authError = null;
                
                console.log('Выход выполнен');
            } catch (error) {
                console.error('Ошибка при выходе:', error);
            }
        },

        async getUserTestData() {
            try{
                const response = await axios.get(`${baseUrl}/user-test`, {
                    withCredentials: true,
                });
                this.userTest = response.data;
                this.user.tests = response.data.tests;
            } catch (error){
                console.log('Ошибка при получении данных:', error)
                throw error;
            }
        },

        async checkAuth() {
            console.log('Проверка авторизации: isAuthenticated = ', this.isAuthenticated);
            if (this.isAuthenticated) {
                try {
                    await this.getUserTestData();
                    return true;
                } catch (e) {
                    console.log('Ошибка поймана, очищаю данные');
                    this.clearData();
                    return false;
                }
            }
            // console.log('isAuthenticated false, запрос не отправлен');
            return false;
        },


        clearData() {
            this.belbinResult = [];
            this.dataBase = [];
            this.admins = [];
            this.userTest = null;
            this.user = null;
            this.isAuthenticated = false;
            this.authError = null;
        }
    },

    getters: {
        getTests: (state) => state.tests,
        getBelbin: (state) => state.belbin,
        getDisc: (state) => state.disc,
        getBelbinResult: (state) => state.belbinResult,
        getDiscResult: (state) => state.discResult,
        getDataBase: (state) => state.dataBase,
        getAdmins: (state) => state.admins,
        getUser: (state) => state.user,
        getUserTest: (state) => state.userTest,
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