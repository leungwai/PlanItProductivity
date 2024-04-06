import axios from 'axios';

const authService = axios.create({
  xsrfCookieName: 'csrf_access_token',
});

const COOKIE_EXPIRED_MSG = 'Token has expired';
authService.interceptors.response.use((response) => (response), async (error) => {
  const errorMessage = error.response.data.msg;
  const err = error;
  switch (err.response.status) {
    case 401:
      if (!err.config.retry && errorMessage === COOKIE_EXPIRED_MSG) {
        err.config.retry = true;
        authService.defaults.xsrfCookieName = 'csrf_refresh_token';
        await authService.post('api/auth/refresh_token');
        authService.defaults.xsrfCookieName = 'csrf_access_token';
        return authService(err.config);
      }
      await this.$store.dispatch('logoutUserState');
      break;
    case 404:
      this.$router.push('/error');
      break;
    default:
      break;
  }
  return error.response;
});

export default authService;
