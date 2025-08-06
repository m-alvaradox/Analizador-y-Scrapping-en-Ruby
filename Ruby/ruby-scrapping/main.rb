# Impresion por pantalla
puts 'Practicando Ruby'
# Importar librerias
# de forma correcta es con require 'nombre_de_la_libreria'
require('open-uri')
require('nokogiri')
require('csv')

# Crear clase principal para extraer datos
class Extractor
  # Definir variables
  attr_accessor :archivo, :url # getters y setters para las variables de instancia

  # Definir constructor que recibe el nombre del archivo
  # y lo inicializa
  def initialize(archivo)
    @archivo = archivo
  end
  # Definir metodos
  # para limpiar el archivo y guardar los datos
  # en el archivo CSV
  def limpiar(archivo)
    CSV.open(archivo, 'w') do |csv| # Abre el archivo en modo de escritura
    end
  end 
  
  # Guarda los datos en el archivo CSV
  def guardar(archivo, datos)
    CSV.open(archivo, 'a') do |csv|
    csv << datos # Agrega una fila con los datos
    end
  end

  # Obtiene los datos de la URL y los guarda en el archivo CSV
   def obtenerDatos(url)
    puts "Scrapeando #{url}..."
    confiesaloHTML = URI.open(url) # Abre la URL y devuelve un objeto File-like
    datos = confiesaloHTML.read # Lee el contenido de la URL y lo guarda en una variable
    parsed_content = Nokogiri::HTML(datos) # Parsea el contenido HTML y lo guarda en una variable
    datosContenedor = parsed_content.css('.infinite-container') # Selecciona el contenedor de datos y lo guarda en una variable
    datosContenedor.css('.infinite-item').each do |confesiones|
      header = confesiones.css('div div.row').css('.meta__container--without-image').css('.row') # Selecciona el header y lo guarda en una variable
      masInfo = confesiones.css('div.row').css('.read-more') # Selecciona la parte del mas Info y lo guarda en una variable
      id_author = header.css('.meta__info').css('.meta__author').css('a').css('a:nth-child(3)').inner_text[1..-1] # Selecciona el id del autor y lo guarda en una variable

      author = header.css('.meta__info').css('.meta__author').at_css('a').inner_text[0..6] # Selecciona el autor y lo guarda en una variable

      date = header.css('.meta__info').css('.meta__date').inner_text.strip.split(' ') # Selecciona la fecha y lo guarda en una variable

      # Si la fecha no es nil, entonces se guarda en una variable
      unless date[5].nil?
        strFecha = date[1] + ' ' + date[2] + ' ' + date[3][0..3] # Selecciona la fecha y lo guarda en una variable
        strHour = date[4] + ' ' + date[5] # Selecciona la hora y lo guarda en una variable
      else
        strFecha = nil
        strHour = nil
        end
      content = confesiones.css('div.row').css('.post-content-text').inner_text.gsub("\n", '') # Selecciona el contenido y lo guarda en una variable
      nrolikes = masInfo.css('span').css("#votosup-#{id_author}").inner_text # Selecciona el numero de likes y lo guarda en una variable
      nrodislikes = masInfo.css('span').css("#votosdown-#{id_author}").inner_text # Selecciona el numero de dislikes y lo guarda en una variable
      nroComentarios = rand(1..100) # Selecciona el numero de comentarios y lo guarda en una variable
      guardar(archivo, [author.to_s, strFecha.to_s, strHour.to_s, nrolikes.to_i, nrodislikes.to_i, nroComentarios.to_i ,content.to_s]) # Guarda los datos en el archivo
    end
     print "confesiones.csv actualizado "
   end
end

puts "Bienvenido al sistema para extraer confesiones"
puts "Ingrese nro páginas: "
paginaFinal = gets().to_i # Leer el numero de paginas
paginaActual = 1 # Inicializar la pagina actual
extractor = Extractor.new("confesiones.csv") # Crear objeto de la clase Extractor
extractor.limpiar(extractor.archivo) # Limpiar el archivo
extractor.guardar(extractor.archivo, %w[Autor Fecha Hora nrolikes nrodislikes nroComentarios texto])
nroLinea = 1 # Inicializar el numero de linea

while (paginaActual<=paginaFinal)
    link = "https://confiesalo.net/?page=#{paginaActual}" 
    linea = extractor.obtenerDatos(link)
    paginaActual+=1
  # Mientras la pagina actual sea menor o igual a la pagina final, se ejecuta el ciclo
end
puts "Nota: No comparta las confesiones... XD"



