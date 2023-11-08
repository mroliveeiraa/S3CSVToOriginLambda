import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.client.TestRestTemplate.HttpClientOption;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.http.ResponseEntity;
import org.springframework.boot.web.client.RestTemplateBuilder;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class XptoControllerIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    public void testRequisicaoPost() {
        // Suponhamos que você tenha uma rota /xpto no seu controlador que lida com a requisição POST
        String url = "/xpto";

        // Aqui você pode configurar o cabeçalho e o payload da requisição
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        // Configurar os cabeçalhos, payload, etc.

        // Executar a requisição POST
        ResponseEntity<String> responseEntity = restTemplate.exchange(
            url, 
            HttpMethod.POST, 
            new HttpEntity<>("seu_payload_aqui", headers), 
            String.class);

        // Adicione as asserções aqui para verificar o comportamento esperado
        // Por exemplo, verificar o status da resposta, conteúdo da resposta, etc.
    }
}
