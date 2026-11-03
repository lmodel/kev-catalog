package example;

/* metamodel_version: 1.12.0 */
/* version: 2026-09-17 */
import java.net.URI;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.util.List;
import lombok.*;

/**
  One published release of the KEV catalog, with the entries it lists.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class KevCatalog  {

  private String title;
  private String catalogVersion;
  private ZonedDateTime dateReleased;
  private int count;
  private List<KevVulnerability> vulnerabilities;


}