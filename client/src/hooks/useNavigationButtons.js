import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import TasksService from "../API/TasksService";

export const useNavigationButtons = () => {
    const { taskId, jobAlias } = useParams()
    const [prevTaskId, setPrevTaskId] = useState();
    const [nextTaskId, setNextTaskId] = useState();
    const [totalTasks, setTotalTasks] = useState(0);
    const [offset, setOffset] = useState(0);
    const navigate = useNavigate();

    const getPaginationData = async () => {
        const res = await TasksService.getNextTaskId(jobAlias, 1, offset);

        if (res.success) {
          if (offset > 0) {
            setPrevTaskId(taskId);
          }
          setTotalTasks(res.data.total_tasks);
          setNextTaskId(res.data.next_task_id);
        }
      }

    useEffect(() => {
        getPaginationData();
    }, [offset]);

    const clickNext = async () => {
        if (nextTaskId == null) {
          return
        }

        navigate(`/annotate/job/${jobAlias}/task/${nextTaskId}`);
        setOffset(offset + 1);
    };

    const clickPrev = async () => {
        if (prevTaskId == null) {
          return
        }

        navigate(`/annotate/job/${jobAlias}/task/${prevTaskId}`);
    };

    return [clickNext, clickPrev, prevTaskId, nextTaskId, totalTasks]
}
