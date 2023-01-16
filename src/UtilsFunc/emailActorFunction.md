### Email Actor function

| Function                           | Hotmail     | Gmail       | Yahoo        | Mailu        |
| ---------------------------------- | ----------- | ----------- | ------------ | ------------ |
| IMAP-TLS connection [ read email ] | N.A         | N.A         | OK           | OK           |
| IMAP-SSL connection [read email]   | OK          | OK          | OK           | N.A          |
| POP-3 connection [read email]      | OK          | OK          | N.A          | N.A          |
| Download attachment [read email]   | OK          | OK          | N.A          | OK           |
| Read Inbox                         | OK          | OK          | OK           | OK           |
| Read outBox                        | OK [Outbox] | OK [Sent]   | OK [out_box] | OK [out_box] |
| Read Junk mail(spam)               | only Text   | N.A [Spam]  | OK           | N.A          |
| SMTP-TLS connection [send email]   | N.A         | OK          | N.A          | OK           |
| SMTP-SSL connection [send email]   | OK          | OK          | OK           | N.A          |
| SendEmail                          | OK          | OK          | OK           | OK           |
| Send Attachment file               | OK [< 10Mb] | OK [< 25Mb] | N.A          | OK           |
| Forward email or forward eml file  | OK          | OK          | OK           | OK           |

