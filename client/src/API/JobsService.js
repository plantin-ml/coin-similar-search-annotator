import axios from "axios";

const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    timeout: 5000,
    headers: {
        "Authorization": "Bearer " + process.env.REACT_APP_API_TOKEN
    }
});

export default class JobsService {

    static async getAllJobs(limit, offset) {
        const response = await axiosInstance.get('/jobs', {
            params: {
                'limit': limit,
                'offset': offset
            }
        })

        return response
    }
}