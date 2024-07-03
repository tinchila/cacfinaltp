import { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const List = ({ url }) => {
    const [list, setList] = useState([]);

    const fetchList = async () => {
        try {
            const response = await axios.get(`${url}/api/bebidas`);
            if (response.status === 200) {
                setList(response.data);
            } else {
                toast.error("Error al obtener la lista de bebidas");
            }
        } catch (error) {
            toast.error("Error al conectar con el servidor");
            console.error("Error:", error);
        }
    };

    const removeBeverage = async (id) => {
        try {
            const response = await axios.delete(`${url}/api/bebidas/${id}`);
            if (response.status === 200) {
                toast.success("Bebida eliminada correctamente");
                fetchList(); // Actualizar la lista después de eliminar
            } else {
                toast.error("Error al eliminar la bebida");
            }
        } catch (error) {
            toast.error("Error al conectar con el servidor");
            console.error("Error:", error);
        }
    };

    useEffect(() => {
        fetchList();
    }, []);

    return (
        <div className='list add flex-col'>
            <p>All Beverages List</p>
            <div className="list-table">
                <div className="list-table-format title">
                    <b>Image</b>
                    <b>Bebida</b>
                    <b>Marca</b>
                    <b>Variedad</b>
                    <b>Precio</b>
                    <b>Cantidad</b>
                    <b>Action</b>
                </div>
                {list.map((item, index) => (
                    <div key={index} className='list-table-format'>
                        <img src={`${url}/images/${item.imagen}`} alt="" />
                        <p>{item.bebida}</p>
                        <p>{item.marca}</p>
                        <p>{item.variedad}</p>
                        <p>${item.precio}</p>
                        <p>{item.cantidad}</p>
                        <p onClick={() => removeBeverage(item.id)} className='cursor'>Remove</p>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default List;
