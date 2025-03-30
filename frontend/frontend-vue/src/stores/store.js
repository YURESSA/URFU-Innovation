import { defineStore } from 'pinia';
import axios from 'axios';


export const baseUrl = 'http://127.0.0.1:5000/'

export const useDataStore = defineStore('data', {
    state: () => ({
        tests: [],
        belbin: [],
        belbinResult: [],
        dataBase: [],
        admins: [],
    }),
    actions: {
        async fetchTests() {
            try {
                const response = await axios.get(`${baseUrl}/api/get-all-test`); // получаю название и url
                this.tests = response.data;
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        async fetchBelbin() {
            try {
                const response = await axios.get(`${baseUrl}/api/belbin-test`, {
                    withCredentials: true,
                }); // получаю вопросы теста
                this.belbin = response.data;
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        async fetchBelbinResult(result) {
            try {
                const response = await axios.post(`${baseUrl}/api/belbin-test`, result, {
                    withCredentials: true,
                }); // получаю результаты теста Белбина
                this.belbinResult = response.data;
                console.log('Результат теста Белбина:', this.belbinResult);
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        async fetchDataBase() {
            try{
                const response = await axios.get(`${baseUrl}/api/get-test-results`, {
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
                const response = await axios.get(`${baseUrl}/api/admins`, {
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
                const response = await axios.delete(`${baseUrl}/api/delete_admin`, {
                    data: { username },
                    withCredentials: true,
                });
                console.log('Ответ сервера:', response.data);
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        async TransferSuperAdmin(username) {
            try {
                const response = await axios.delete(`${baseUrl}/api/promote-to-super-admin`, {
                    data: { username },
                    withCredentials: true,
                }); 
                console.log(response.data)
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
    },
    getters: {
        getTests: (state) => state.tests,
        getBelbin: (state) => state.belbin,
        getBelbinResult: (state) => state.belbinResult,
        getDataBase: (state) => state.dataBase,
        getAdmins: (state) => state.admins
    },
    persist: {
        key: 'data-store',
        storage: window.localStorage,
        paths: ['tests', 'belbin', 'belbinResult'],
    },
});
