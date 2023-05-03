import {
    CarryOutOutlined,
    BarsOutlined,
    AppstoreOutlined
} from '@ant-design/icons';
import { Layout, Menu } from 'antd';
import React, { useState } from 'react';
import TasksTable from '../components/Tasks/TasksTable';

const { Footer, Header, Sider, Content } = Layout;

const TasksPage = () => {
    return (
        <TasksTable />
    );
};

export default TasksPage;