package None;

/* metamodel_version: 1.7.0 */
/* version: 1.0 */
import java.util.List;
import lombok.*;

/**
  The CISA Known Exploited Vulnerabilities (KEV) Catalog — the authoritative source of vulnerabilities confirmed exploited in the wild, maintained by CISA per Binding Operational Directive (BOD) 22-01.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class KevCatalog  {

  private String title;
  private String catalogVersion;
  private String dateReleased;
  private Integer count;
  private List<KevEntry> vulnerabilities;

}