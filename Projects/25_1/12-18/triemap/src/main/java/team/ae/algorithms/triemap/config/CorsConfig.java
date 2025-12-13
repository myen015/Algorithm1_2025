package team.ae.algorithms.triemap.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.filter.CorsFilter;

@Configuration
public class CorsConfig {

    @Bean
    public CorsFilter corsFilter() {
        var cfg = new org.springframework.web.cors.CorsConfiguration();
        cfg.addAllowedOriginPattern("http://192.168.*.*:5174");
        cfg.addAllowedOriginPattern("http://192.168.*.*:5173");
        cfg.addAllowedOriginPattern("http://localhost:5174");
        cfg.addAllowedOriginPattern("http://localhost:5173");
        cfg.addAllowedMethod("*");
        cfg.addAllowedHeader("*");
        cfg.setAllowCredentials(true);
        var src = new org.springframework.web.cors.UrlBasedCorsConfigurationSource();
        src.registerCorsConfiguration("/**", cfg);
        return new org.springframework.web.filter.CorsFilter(src);
    }

}
