import { defineStore } from 'pinia';
import axios from 'axios';

export const useDataStore = defineStore('data', {
    state: () => ({
        tests: [],
        belbin: [],
        belbinResult: [],
    }),
    actions: {
        async fetchTests() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/get-all-test', {
                    withCredentials: true,
                }); // получаю название и url
                this.tests = response.data;
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
        async fetchBelbin() {
            try {
                const response = await axios.get('http://localhost:5000/api/belbin-test', {
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
                const response = await axios.post('http://localhost:5000/api/belbin-test', result, {
                    withCredentials: true,
                }); // получаю результаты теста Белбина
                this.belbinResult = response.data;
                console.log('Данные загрузил');
            } catch (error) {
                console.error('Ошибка при получении данных:', error);
            }
        },
    },
    getters: {
        getTests: (state) => state.tests,
        getBelbin: (state) => state.belbin,
        getBelbinResult: (state) => state.belbinResult,
    },
    persist: {
        key: 'data-store',
        storage: window.localStorage,
        paths: ['tests', 'belbin', 'belbinResult'],
    },
});
