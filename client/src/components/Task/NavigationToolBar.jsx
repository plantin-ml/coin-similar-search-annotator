import { ClockCircleOutlined, LeftOutlined, RightOutlined, StopOutlined, LoadingOutlined } from '@ant-design/icons';
import { Badge, Button, Col, Layout, Row, Select, Space, Spin } from 'antd';
import { zonedTimeToUtc } from 'date-fns-tz';
import formatDistance from 'date-fns/formatDistance';
import parseJSON from 'date-fns/parseJSON';
import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import TasksService from "../../API/TasksService";

const { Header, Content, Sider } = Layout;
const { Option } = Select;


function NavigationToolBar({ task, limit, onChangeLimit, isLoading, fetchError }) {
  const { taskId, jobAlias } = useParams()
  const [offset, setOffset] = useState(0);
  const [prevTaskId, setPrevTaskId] = useState();
  const [totalTasks, setTotalTasks] = useState(0);
  const [nextTaskId, setNextTaskId] = useState();
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

  const skipClick = async () => {
    await TasksService.changeStateForTask(taskId, 'skipped');
    clickNext();
  };

  const getDiffUpdatedAt = (updated_at) => {
    return formatDistance(
      zonedTimeToUtc(parseJSON(updated_at), 'Europe/Kyiv'),
      zonedTimeToUtc(new Date()), { addSuffix: true }
    )
  }

  const GetStateBadge = (state) => {
    console.log(state)
    const mapStateToBadge = {
      'draft': <Badge status="default" text="Draft" />,
      'skipped': <Badge status="warning" text="Skipped" />,
      'annotated': <Badge status="processing" text="Annotated" />,
      'done': <Badge status="success" text="Done" />,
      'ready': <Badge status="success" text="Ready" />,
      'error': <Badge status="error" text="Error" />,
      'merged': <Badge status="error" text="MERGED" />,
    }

    return mapStateToBadge[state]
  }

  const headerStyle = {
    color: '#fff',
    height: 64,
    paddingInline: 50,
    lineHeight: '64px',
    backgroundColor: '#7dbcea',
    position: 'sticky',
    zIndex: 1,
    width: '100%',
  };
  const antLoadingIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;
  return (
      <>
        <Header style={headerStyle}>
            <Row justify="left" >
              <Col span={18}>
                <Space wrap>
                    <Button disabled={prevTaskId == null} onClick={clickPrev} type="primary" icon={<LeftOutlined />} />
                    <span>Task: {taskId} / ({ totalTasks })</span>
                    {nextTaskId && <Button onClick={clickNext} type="primary" icon={<RightOutlined />} />}
                    {task && task.state == 'draft' && <Button danger onClick={skipClick} type="primary" icon={<StopOutlined />} >Skip</Button>}
                    {task && task.state && GetStateBadge(task.state)}
                    {task && task.updated_at && (<><ClockCircleOutlined className="timeline-clock-icon" /> Updated at: {getDiffUpdatedAt(task.updated_at)}</>)}
                </Space>
              </Col>
              <Col span={6}>
                  <Space wrap>
                    <span>Limit:</span>
                    <Select value={limit} defaultValue="100" style={{ width: 80 }} onChange={ onChangeLimit }>
                        <Option value="5">5</Option>
                        <Option value="10">10</Option>
                        <Option value="50">50</Option>
                        <Option value="100">100</Option>
                        <Option value="150">150</Option>
                        <Option value="200">200</Option>
                    </Select>
                    {isLoading && <span><Spin indicator={antLoadingIcon} />Loading...</span>}
                  </Space>
              </Col>
            </Row>
        </Header>
      </>
  );
}

export default NavigationToolBar;