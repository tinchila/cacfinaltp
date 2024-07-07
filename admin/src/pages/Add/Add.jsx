import { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import './Add.css'

const Add = ({ url }) => {
    const [data, setData] = useState({
        bebida: "",
        marca: "",
        variedad: "",
        precio: "",
        imagen: null,
        cantidad: ""
    });

    const onChangeHandler = (event) => {
        const { name, value } = event.target;
        setData({ ...data, [name]: value });
    };

    const onFileChangeHandler = (event) => {
        setData({ ...data, imagen: event.target.files[0] });
    };

    const onSubmitHandler = async (event) => {
        event.preventDefault();
        try {
            const formData = new FormData();
            formData.append('bebida', data.bebida);
            formData.append('marca', data.marca);
            formData.append('variedad', data.variedad);
            formData.append('precio', data.precio);
            formData.append('imagen', data.imagen);
            formData.append('cantidad', data.cantidad);

            const config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            };

            const response = await axios.post(`${url}/api/bebidas`, formData, config);
            if (response.status === 201) {
                toast.success('Bebida agregada correctamente');
                setData({
                    bebida: '',
                    marca: '',
                    variedad: '',
                    precio: '',
                    imagen: null,
                    cantidad: ''
                });
            } else {
                toast.error('Error al agregar la bebida');
            }
        } catch (error) {
            toast.error('Error al conectar con el servidor');
            console.error('Error:', error);
        }
    };

    return (
        <div className='add'>
            <form className='flex-col' onSubmit={onSubmitHandler}>
                <div className="add-img-upload flex-col">
                    <p>Upload Image</p>
                    <label htmlFor="image">
                        <img src={data.imagen ? URL.createObjectURL(data.imagen) : '/upload_area.png'} alt="" />
                    </label>
                    <input onChange={onFileChangeHandler} type="file" id="image" hidden required />
                </div>
                <div className="add-product-name flex-col">
                    <p>Bebida</p>
                    <input onChange={onChangeHandler} value={data.bebida} type="text" name='bebida' placeholder='Nombre de la bebida' />
                </div>
                <div className="add-product-description flex-col">
                    <p>Marca</p>
                    <input onChange={onChangeHandler} value={data.marca} type="text" name="marca" placeholder='Marca de la bebida' required />
                </div>
                <div className="add-category-price">
                    <div className="add-category flex-col">
                        <p>Variedad</p>
                        <input onChange={onChangeHandler} value={data.variedad} type="text" name="variedad" placeholder='Variedad de la bebida' />
                    </div>
                    <div className="add-price flex-col">
                        <p>Precio</p>
                        <input onChange={onChangeHandler} value={data.precio} type="number" name='precio' placeholder='Precio de la bebida' />
                    </div>
                    <div className="add-quantity flex-col">
                        <p>Cantidad</p>
                        <input onChange={onChangeHandler} value={data.cantidad} type="number" name='cantidad' placeholder='Cantidad de la bebida' />
                    </div>
                </div>
                <button type='submit' className='add-btn'>ADD</button>
            </form>
        </div>
    );
};

export default Add;
