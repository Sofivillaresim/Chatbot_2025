#LIBRERIAS 
import groq
import streamlit as st #! API ->  pip -> plataforma donde se va a encontrar nuestra pagina web

#! ----------------------------------------------------------------- VARIABLES ----------------------------------------------------------------
altura_contenedor_chat = 600
streamstatus = True

#numero = random.randint(0,10)
#print(numero)

# Cambiar apodos a las librerias para que sea mas facil.
# import random as Rm

#! ------------------------------------------------------------------ LA PÁGINA: --------------------------------------------------------------


#CONSTANTES
MODELOS = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile","meta-llama/llama-guard-4-12b"]   #& variables "minuscula" constantes "mayuscula" (no cambian. no hay que modificarlos)


#! ------------------------------------------------------------------- FUNCIONES --------------------------------------------------------------

#ESTA FUNCION UTILIZA STREAMLIT PARA CREAR LA INTERFAZ DE LA PAGINA Y ADEMAS RETORNA EL MODELO ELEGIDO POR EL USUARIO
def configurar_pagina():
 
    st.set_page_config(page_title="Sofia IA", page_icon= "❤")

    st.title ("Sofia IA")

    #nombre = st.text_input ("¿Cuál es tu nombre?")

    #if st.button("Saludar"):
     #st.write("Hola " + nombre)

    st.sidebar.title("Selección de modelos")

    elegirmodelo = st.sidebar.selectbox("Elegí un modelo ", options=MODELOS, index=0)

    return elegirmodelo


#ESTA FUNCIÓN LLAMA A st.secrets PARA OBTENER LA CLAVE DE LA API DE GROQ Y CREA UN USUARIO
def crear_usuario():
    clave_secreta = st.secrets["CLAVE_API"]
    return groq.Groq(api_key = clave_secreta)

#ESTA FUNCIÓN CONFIGURA EL MODELO DE LENGUAJE PARA QUE PROCESE EL PROMPT DEL USUARIO
def configurar_modelo(cliente, modelo_elegido, prompt_usuario):
    return cliente.chat.completions.create(
       model = modelo_elegido,
       messages = [{"role" : "user", "content" : prompt_usuario}], #diccionario 
       stream = streamstatus #ver como el chat escribe
    )

# CREAMOS UNA SESIÓN LLAMADA "mensajes" QUE VA A GUARDAR LO QUE LE ESCRIBIMOS LA CHATBOT
def inicializar_estado():
   if "mensajes" not in st.session_state:
      st.session_state.mensajes = [] #los corchetes crean una lista 


def actualizar_historial (rol, contenido, avatar):
    st.session_state.mensajes.append({"role" : rol, "content" : contenido, "avatar" : avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.write(mensaje["content"])

def area_chat(): 
    contenedor = st.container(height=altura_contenedor_chat, border=True)
    with contenedor:
            mostrar_historial ()

def generar_respuesta(respuesta_completa_del_bot):
    _respuesta_posta = "" 
    for frase in respuesta_completa_del_bot:
        if frase.choices[0].delta.content:
            _respuesta_posta += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return _respuesta_posta

#! ------------------------------------------------------------------- IMPLEMENTACIÓN ---------------------------------------------------------------------------

def main():

    modelo_elegido_por_el_usuario = configurar_pagina()

    cliente_usuario = crear_usuario()

    inicializar_estado()

    area_chat()

    prompt_del_usuario = st.chat_input("Escribí tu consulta: ")

    if prompt_del_usuario:
        actualizar_historial("user", prompt_del_usuario, "🤗")
        respuesta_del_bot = configurar_modelo(cliente_usuario, modelo_elegido_por_el_usuario, prompt_del_usuario)
        
        if respuesta_del_bot:
                with st.chat_message("assistant"):
                    respuesta_posta = st.write_stream(generar_respuesta(respuesta_del_bot))
                    actualizar_historial ("assistant", respuesta_posta, "🤖")
        
                    st.rerun()  
   
if __name__ == "__main__":
    main()