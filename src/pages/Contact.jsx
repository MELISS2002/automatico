import React, { useState } from 'react';
import './Contact.css';  // Asegúrate de tener un archivo CSS para los estilos

const Contact = () => {
  // Estados para manejar los valores del formulario
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });

  // Estado para manejar el estado de envío
  const [isSubmitted, setIsSubmitted] = useState(false);

  // Función para manejar el cambio en los inputs del formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  // Función para manejar el envío del formulario
  const handleSubmit = (e) => {
    e.preventDefault();
    // Aquí podrías agregar lógica para enviar los datos al servidor
    console.log('Formulario enviado', formData);
    setIsSubmitted(true);  // Cambiar el estado a enviado
  };

  return (
    <div className="contact-page-container">
      <center><h1 className="page-title">Contacto</h1></center>
      
      {/* Mostrar mensaje de confirmación si el formulario fue enviado */}
      {isSubmitted && <p>Gracias por tu mensaje. Nos pondremos en contacto contigo pronto.</p>}

 
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Nombre</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="email">Correo Electrónico</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="message">Mensaje</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            required
          />
        </div>
        
        <button type="submit">Enviar Mensaje</button>
      </form>
    </div>
  );
};

export default Contact;
