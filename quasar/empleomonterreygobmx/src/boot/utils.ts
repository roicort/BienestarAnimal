/***********/
/* Getters */
/***********/

import {apiAdopta, apiIde, apiMty} from 'boot/axios'
import {OAuthProvider, signInWithPopup} from 'firebase/auth'
import {firebaseAuth} from 'boot/firebase'

// Vacantes --------------------------------------------------------------

async function getPadron() {

  const response = await apiAdopta.get('/animales/padron/')

  response.data.forEach(function (obj: any) {
    obj.label = obj.nombre
    delete obj.nombre
    obj.value = obj.id
  })

  return response.data;

}

async function getAdopciones() {

  const response = await apiAdopta.get('/animales/adopciones/')

  response.data.forEach(function (obj: any) {
    obj.label = obj.nombre
    delete obj.nombre
    obj.value = obj.id
  })

  return response.data;

}

async function getMisAnimales(accessToken: string, vinculaciones: any) {

  const asociaciones: any = []
  vinculaciones.forEach(function (obj: any) {  asociaciones.push(obj.asociacion) })
  let response = {data: []}

  if (asociaciones && asociaciones.length > 0) {
    let petition  = '/animales/padron/?'
    asociaciones.forEach(function (obj: any) { petition += 'asociacion=' + obj + '&' })
    petition = petition.slice(0, -1)
    response = await apiAdopta.get(petition,
      {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
    )
  }

  response.data.forEach(function (obj: any) {
    obj.label = obj.nombre
    delete obj.nombre
    obj.value = obj.id
  })

  return response.data;

}

async function getEnAdopcion(accessToken: string, vinculaciones: any) {

  const asociaciones: any = []
  vinculaciones.forEach(function (obj: any) {  asociaciones.push(obj.asociacion) })
  let response = {data: []}

  if (asociaciones && asociaciones.length > 0) {
    let petition  = '/animales/adopciones/?'
    asociaciones.forEach(function (obj: any) { petition += 'asociacion=' + obj + '&' })
    petition = petition.slice(0, -1)
    response = await apiAdopta.get(petition,
      {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
    )
  }

  response.data.forEach(function (obj: any) {
    obj.label = obj.nombre
    delete obj.nombre
    obj.value = obj.id
  })

  return response.data;

}

async function getPerdidos(accessToken: string, vinculaciones: any) {

  const asociaciones: any = []
  vinculaciones.forEach(function (obj: any) {  asociaciones.push(obj.asociacion) })
  let response = {data: []}

  if (asociaciones && asociaciones.length > 0) {
    let petition  = '/animales/reportes/?'
    asociaciones.forEach(function (obj: any) { petition += 'asociacion=' + obj + '&' })
    petition = petition.slice(0, -1)
    response = await apiAdopta.get(petition,
      {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
    )
  }

  response.data.forEach(function (obj: any) {
    obj.label = obj.nombre
    delete obj.nombre
    obj.value = obj.id
  })

  return response.data;

}

async function getFavoritos(accessToken: string) {
  const response = await apiAdopta.get('/animales/animal-favorito/',
    {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
  )
  return response.data
}

async function getPostulados(accessToken: string) {
  const response = await apiAdopta.get('/animales/postulacion-adopcion/',
    {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
  )
  response.data.forEach(function (obj: any) {
    obj.value = obj.id
    delete obj.id
  })
  return response.data
}

async function getMisPostulaciones(accessToken: string) {
  const response = await apiAdopta.get('/animales/mis-postulaciones/',
    {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
  )
  response.data.forEach(function (obj: any) {
    obj.value = obj.id
    delete obj.id
  })
  return response.data
}

async function getHabilidades() {
  const response = await apiAdopta.get('base/habilidad/')
  response.data.forEach(function (obj: any) {
    obj.label = obj.nombre
    delete obj.nombre
    obj.value = obj.id
    delete obj.id
  })
  return response.data
}

async function getCategorias() {
  const response = await apiAdopta.get('/animales/animal-categoria/')
  response.data.forEach(function (obj: any) {
    obj.label = obj.nombre
    delete obj.nombre
    obj.value = obj.id
    delete obj.id
  })
  return response.data
}

async function getInclusiones() {
  const response = await apiAdopta.get('/animales/animal-inclusion/')
  response.data.forEach(function (obj: any) {
    obj.label = obj.nombre
    delete obj.nombre
    obj.value = obj.id
    delete obj.id
  })
  return response.data
}

async function getDetalleAnimal(accessToken: string, animal_id: number) {
  if (accessToken) {
    const response = await apiAdopta.get(`/animales/padron/${animal_id}/`,
      {
        headers: {
          'Authorization': 'Bearer ' + accessToken,
        }
      }
    )
    return response.data
  } else {
    const response = await apiAdopta.get(`/animales/padron/${animal_id}/`)
    return response.data
  }
}

/*async function getDetalleEmpresa(accessToken: string, asociacion_id: number) {
  const response = await apiAdopta.get(`/asociaciones/asociacion/${asociacion_id}/`,
  {
    headers: {
      'Authorization': 'Bearer ' + accessToken,
    }
  }
  )
  return response.data
}*/

// SCIAN -----------------------------------------------------------------

async function getSubsectorSCIAN() {

  const response = await apiMty.get('/scian/subsector/')
  response.data.results.forEach(function (obj: any) {
    obj.label = obj.nombre
    //delete obj.titulo
    obj.value = obj.clave
    //delete obj.codigo
  })
  return response.data.results
}

async function getClaseSCIAN() {
  const response = await apiMty.get('/scian/clase/?limit=1084&fields=codigo,titulo')
  response.data.results.forEach(function (obj: any) {
    obj.label = obj.nombre
    delete obj.nombre
    obj.value = obj.clave
    delete obj.clave
  })
  return response.data.results
}


// Empresas --------------------------------------------------------------

async function getAsociaciones(accessToken: string, asociacion_id: number) {
  const response = await apiAdopta.get(`/asociaciones/asociacion/${asociacion_id ? asociacion_id : ''}`,
    {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
  )
  response.data.forEach(function (asociacion: any) {
    asociacion.label = asociacion.nombre
    delete asociacion.nombre
    asociacion.value = asociacion.id
    delete asociacion.id
  })
  return response.data
}

async function getSucursales(accessToken: string, asociacion_id: number) {
  const response = await apiAdopta.get(`/asociaciones/centro/${asociacion_id ? '?asociacion=' + asociacion_id : ''}`,
    {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
  )
  response.data.forEach(function (obj: any) {
    obj.label = obj.nombre
    //delete obj.nombre
    obj.value = obj.id
    delete obj.id
  })

  // Solución temporal

  const filtered_response = response.data.filter((sucursal: any) => {
    return sucursal.asociacion == asociacion_id
  })

  return filtered_response
}

async function getVinculaciones(accessToken: string, asociacion_id: number) {
  const response = await apiAdopta.get(`/asociaciones/vinculacion-asociacion/${asociacion_id ? '?asociacion=' + asociacion_id : ''}`,
    {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
  )

  // Solución temporal

  const filtered_response = response.data.filter((sucursal: any) => {
    return sucursal.asociacion === asociacion_id
  })

  return filtered_response
}

async function getDetalleSucursal(accessToken: string, sucursal_id: number) {
  const response = await apiAdopta.get(`/asociaciones/sucursal/${sucursal_id}/`,
    {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
  )

  return response.data
}


// IDE --------------------------------------------------------------

async function getEstados() {
  const response = await apiIde.get('/marco-geoestadistico-inegi/estado/?fields=nombre,clave_geoestadistica&limit=777')
  response.data.results.forEach((estado: any) => {
    estado.label = estado.nombre
    delete estado.nombre
    estado.value = estado.clave_geoestadistica
    delete estado.clave_geoestadistica
  })
  return response.data.results
}

async function getMunicipios(estado: string) {
  const response = await apiIde.get('marco-geoestadistico-inegi/municipio/?estado=' + estado + '&fields=nombre,clave_geoestadistica&limit=777')
  response.data.results.forEach((municipio: any) => {
    municipio.label = municipio.nombre
    delete municipio.nombre
    municipio.value = municipio.clave_geoestadistica
    delete municipio.clave_geoestadistica
  })
  return response.data.results
}

async function getLocalidades(municipio: string) {

  const response = await apiIde.get('marco-geoestadistico-inegi/localidad/?municipio=' + municipio + '&fields=nombre,clave_geoestadistica&limit=777')
  response.data.results.forEach((localidad: any) => {
    localidad.label = localidad.nombre
    delete localidad.nombre
    localidad.value = localidad.clave_geoestadistica
    delete localidad.clave_geoestadistica
  })
  return response.data.results
}

// Auth --------------------------------------------------------------

const loginOIDC = ($q: any) => {
      $q.loading.show({
        message: 'Iniciando sesión, por favor espera...',
      })
      try {
        const provider = new OAuthProvider('oidc.empleo.monterrey.gob.mx')
        signInWithPopup(firebaseAuth, provider)
      } catch (error) {
        console.log('error', error)
        $q.notify({
          color: 'negative',
          message:
            'Ocurrió un error al iniciar sesión, por favor intenta de nuevo.',
          icon: 'report_problem',
          position: 'top',
          timeout: 3000,
        })
      } finally {
        $q.loading.hide()
      }
    }

// Perfil --------------------------------------------------------------

async function getPerfil(accessToken: string, user_id: string) {
  const response = await apiAdopta.get(`/perfiles/perfil-general/${user_id}/`,
    {
      headers: {
        'Authorization': 'Bearer ' + accessToken,
      }
    }
  )
  return response.data
}

async function getGeneros() {
  const response = await apiMty.get('/base/genero/')
  response.data.results.forEach((genero: any) => {
    genero.label = genero.nombre
    delete genero.nombre
    genero.value = genero.id
    delete genero.id
  })
  return response.data.results
}

// -----------------------------------------------------------------

export {
  getAsociaciones,
  getMisAnimales,
  getSucursales,
  getEstados,
  getMunicipios,
  getLocalidades,
  getHabilidades,
  getCategorias,
  getInclusiones,
  getSubsectorSCIAN,
  getClaseSCIAN,
  getVinculaciones,
  getPadron,
  getDetalleSucursal,
  getFavoritos,
  getPostulados,
  getDetalleAnimal,
  loginOIDC,
  getPerfil,
  getMisPostulaciones,
  getGeneros,
  getEnAdopcion,
  getAdopciones,
  getPerdidos
}