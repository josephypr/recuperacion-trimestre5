import cloudinary.uploader

cloudinary.config(
    cloud_name='dr8dcla9c',
    api_key='462582264781828',
    api_secret='OzfGImdVEAemsNu0ziP3P_2lCy8'
)

def subir_a_cloudinary(archivo):
    resultado = cloudinary.uploader.upload(archivo)
    return resultado['secure_url']
