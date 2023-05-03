import React, { useState } from 'react';
import { Routes, Route } from "react-router-dom";
import {
    CarryOutOutlined,
    BarsOutlined,
    AppstoreOutlined
} from '@ant-design/icons';
import { Layout, Menu } from 'antd';
import { Link } from "react-router-dom";
import Task from './pages/Annotator';
import TasksPage from './pages/Tasks';
import JobsPage from './pages/Jobs';

import Home from './pages/Home';
import 'antd/dist/reset.css';
import './styles/App.css';

const { Footer, Header, Sider, Content } = Layout;

const App = () => {
    const [collapsed, setCollapsed] = useState(false);

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
                <Menu
                    theme="dark"
                    mode="inline"
                    defaultSelectedKeys={['1']}
                    items={[
                        {
                            key: '2',
                            icon: <AppstoreOutlined />,
                            label: <Link to='/'>Home</Link>,
                        },
                        {
                            key: '1',
                            icon: <BarsOutlined />,
                            label: <Link to='/jobs'>Jobs</Link>,
                        },
                        // {
                        //     key: '3',
                        //     icon: <CarryOutOutlined />,
                        //     label: 'Jobs',
                        // },
                    ]}
                />
            </Sider>
            <Layout className="site-layout">
                <Content
                    style={{
                        padding: 10,
                        minHeight: 280
                    }}
                >
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/jobs" element={<JobsPage />} />
                        <Route path="/tasks/job/:jobAlias" element={<TasksPage />} />
                        <Route path="/annotate/job/:jobAlias/task/:taskId" element={<Task />} />
                    </Routes>
                </Content>
            </Layout>
        </Layout>
    );
};

export default App