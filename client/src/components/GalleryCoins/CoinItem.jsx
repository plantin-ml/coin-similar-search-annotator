import { Card, Checkbox, Image, Badge, Button } from 'antd';
import cl from "./GalleryCoins.module.css";
import { SearchOutlined } from '@ant-design/icons';

const { Meta } = Card;

export default function CoinItem({ coin, active, onSelect, onSelectCategory }) {

    return (
        <div className={`${cl.imageItem} ${active ? cl.imageItemActive: ''}`} >

            <p onClick={() => { onSelect(coin) }} className={cl.itemTitle}>
                <Checkbox checked={active} />
                { parseFloat(coin.score).toFixed(3) } {coin.denomination}
            </p>

            <Image src={coin.img_url} width={224} height={224} />
            <p></p>
            <p>Category ID: {coin.cat_id}
                {coin.cat_count && <Badge color='#faad14' count={coin.cat_count} />}
                <Button onClick={() => onSelectCategory(coin.cat_id)} style={{ marginLeft: 10 }} shape="circle" icon={<SearchOutlined />} />
            </p>
            <p>Country: {coin.country}</p>
            <p>Year: {coin.year}</p>
        </div>
    );
};