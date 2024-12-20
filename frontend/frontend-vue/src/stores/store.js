import { defineStore } from 'pinia';
import axios from 'axios';


export const baseUrl = 'http://localhost:5000'

export const useDataStore = defineStore('data', {
    state: () => ({
        tests: [],
        belbin: [],
        belbinResult: [],
        dataBase: [],
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
                console.log('Данные загрузил');
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
                console.log('Данные загрузил');
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
                console.log('Данные получены')
            } catch (error){
                console.log('Ошибка при получении данных:', error)
                throw error;
            }
        }
    },
    getters: {
        getTests: (state) => state.tests,
        getBelbin: (state) => state.belbin,
        getBelbinResult: (state) => state.belbinResult,
        getDataBase: (state) => state.dataBase
    },
    persist: {
        key: 'data-store',
        storage: window.localStorage,
        paths: ['tests', 'belbin', 'belbinResult'],
    },
});
