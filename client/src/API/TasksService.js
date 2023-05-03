import axios from "axios";

const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
    timeout: 5000,
    headers: {
        "Authorization": "Bearer " + process.env.REACT_APP_API_TOKEN
    }
});

export default class TasksService {

    static async getAllTasks(jobAlias, limit, offset) {
        const response = await axiosInstance.get(`/tasks/job/${jobAlias}`, {
            params: {
                'limit': limit,
                'offset': offset

            }
        })

        return response
    }

    static async getTaskById(taskId) {
        const response = await axiosInstance.get(`/tasks/${taskId}`)

        return response
    }

    static async getNextTaskId(jobAlias, limit, offset, prevTaskId) {
        const response = await axiosInstance.get('/task/get_next', {
            params: {
                'job_alias': jobAlias,
                'limit': limit,
                'offset': offset,
                'prev_task_id': prevTaskId,
            }
        })

        return response.data
    }

    static async changeStateForTask(taskId, state) {
        const response = await axiosInstance.patch('/tasks/change_state',
            {
                'task_alias': taskId,
                'state': state
            }
        )

        return response
    }

    static async getGalleryCoinsByTaskId(taskId, limit) {
        const response = await axiosInstance.get(`/tasks/${taskId}/gallery_coins_by_task`, {
            params: {
                'limit': limit
            }
        })

        return response
    }

    static async saveAnnotatedTask(taskId, seletedItems) {
        const response = await axiosInstance.post(`/tasks/${taskId}/save_annotations`,
            {
                'annotation_image_ids': seletedItems
            }
        )

        return response
    }

    static async saveTag(taskId, tag) {
        const response = await axiosInstance.post(`/tasks/${taskId}/add_tags`,
            {
                'tags': [tag]
            }
        )

        return response
    }
}