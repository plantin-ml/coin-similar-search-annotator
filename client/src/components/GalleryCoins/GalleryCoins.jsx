import { CheckCircleOutlined } from '@ant-design/icons';
import { Badge, Button, Col, Row } from 'antd';
import React from "react";
import CoinItem from "./CoinItem.jsx";
import cl from "./GalleryCoins.module.css";


export default function GalleryCoins({ coins, onSelectItem, selecteds, onSelectAll, onSelectCategory = () => {} }) {
    const groupedCoinsByCategory = coins.reduce((acc, coin) => {
        if (acc[coin.cat_id] === undefined) {
            acc[coin.cat_id] = []
        }
        acc[coin.cat_id].push(coin)

        return acc
    }, {})

    const GetGroupedCoin = (coins) => {
        if (coins.length <= 1) {
            return (
                <>
                    { coins.map(coin => <CoinItem onSelectCategory={onSelectCategory} onSelect={ onSelectItem } active={selecteds.includes(coin.id)} coin={coin} key={coin.id} />) }
                </>
            )
        } else if (coins.length >= 2) {
            return (
                <div>
                    <div className={cl.coinGroupToolbar}>
                        <Badge count={coins.length}></Badge>
                        <Button type="dashed" shape="circle" icon={<CheckCircleOutlined />} onClick={ () => onSelectAll(coins) } />
                    </div>
                    <div className={cl.coinGroup}>
                        {coins.map(coin => {
                            coin['count'] = coins.length
                            return <CoinItem onSelectCategory={onSelectCategory} onSelect={ onSelectItem } active={ selecteds.includes(coin.id) } coin={coin} key={coin.id} />
                        })}
                    </div>
                </div>
            )
        }
    }
    const mySort = (a, b) => {
        if (Math.min(...a.map(i=>i.score)) > Math.min(...b.map(i=>i.score))) {
            return 1;
        }
        if (Math.min(...a.map(i=>i.score)) < Math.min(...b.map(i=>i.score))) {
            return -1;
        }
        return 0;
    }

    return (
        <>
            <Row justify="center">
                <Col span={24}>
                    <div className={cl.mainImageListContainer}>
                        <div className={cl.imageListContainer}>
                            {Object.values(groupedCoinsByCategory).sort(mySort).map(coins => {
                                return GetGroupedCoin(coins)
                            }) }
                        </div>
                    </div>
                </Col>
            </Row>
        </>
    );
};