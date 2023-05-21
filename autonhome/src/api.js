import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/';

export async function getAccessToken(username, password) {
  try {
    const response = await axios.post(`${BASE_URL}token/`, {
      username: username,
      password: password,
    });
    
    return response.data.access;
  } catch (error) {
    console.error(`Error during authentication: ${error}`);
  }
}

// export async function getMeasures(token) {
//   try {
//     const response = await axios.get(`${BASE_URL}measures/`, {
//       headers: {
//         Authorization: `Bearer ${token}`,
//       },
//     });
//     return response.data;
//   } catch (error) {
//     console.error(`Error during fetching measures: ${error}`);
//   }
// }

export async function getMeasures(token) {
  try {
    const response = await axios.get(`${BASE_URL}measures/`, {
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    
    return response.data;
  } catch (error) {
    console.error(`Error during fetching measures: ${error}`);
  }
}



export async function postLogin(token, username, password) {
  try {
    const response = await axios.post(`${BASE_URL}auth/login/`, {
      username,
      password
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error(`Error during login: ${error}`);
  }
}

  