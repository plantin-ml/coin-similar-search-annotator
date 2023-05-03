import axios from "axios";

const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    timeout: 5000,
    headers: {
        Authorization: "Bearer " + process.env.REACT_APP_API_TOKEN
    }
});

export default class CoinDataService {

    static async getAllByCoinId(coinId) {
        const response = await axiosInstance.get('/coin_data', {
            params: {
                'category_id': coinId,
            }
        })

        return response
    }
}