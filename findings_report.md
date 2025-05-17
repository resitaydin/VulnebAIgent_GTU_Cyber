# Vulnerability Assessment Report  
**Target:** scanme.nmap.org (45.33.32.156)  
**Assessment Focus:** SSH (Port 22)  
**Scanner Used:** Nmap 7.95 (Nmap Scripting Engine only)  
**Scan Date:** 2025-05-17  

---

## Executive Summary

A comprehensive vulnerability assessment was performed on scanme.nmap.org, specifically targeting port 22 (SSH), with all enumeration and exploitation checks restricted to the use of Nmap and its publicly available NSE scripts. The objectives were to identify any exploitable vulnerabilities, weak configurations, or insecure protocols/ciphers available on the target’s SSH service.

**Key Results:**
- **SSH service is running**: OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (outdated; protocol 2.0 only).
- **No exploitable vulnerabilities were detected by Nmap’s available vulnerability scripts**, including generic and CVE-focused checks.
- **No insecure (SSHv1) protocol support was found.**
- **Multiple cryptographic algorithms (including some legacy/weak ones) are supported**; these are enumerated below.
- **Nmap’s coverage is limited**: Many known vulnerabilities affecting OpenSSH 6.6.1p1 cannot be detected by Nmap scripts. Manual research or specialized vulnerability scanners are advised for a definitive determination.

---

## Scan Methodology

All assessment steps were performed strictly within the confines of Nmap’s standard and script-driven capabilities:

1. **Port Availability**  
   ```
   nmap -p 22 scanme.nmap.org
   ```
   - Confirmed SSH (TCP 22) is open.

2. **Service and Version Fingerprinting**  
   ```
   nmap -sV -p 22 scanme.nmap.org
   ```
   - Identified the running service as OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (protocol 2.0 only).

3. **SSH Protocol and Cipher Enumeration**  
   ```
   nmap --script=sshv1 -p 22 scanme.nmap.org
   nmap --script=ssh2-enum-algos -p 22 scanme.nmap.org
   ```
   - Checked for legacy protocol support (SSHv1).
   - Enumerated supported key exchange, host key, cipher, and MAC algorithms.

4. **Authentication Methods and Host Key Collection**  
   ```
   nmap --script=ssh-auth-methods -p 22 scanme.nmap.org
   nmap --script=ssh-hostkey -p 22 scanme.nmap.org
   ```
   - Listed public key and password authentication support.
   - Collected all public host key fingerprints.

5. **User Enumeration and Brute Force (Attempted)**  
   ```
   nmap --script=ssh-brute,ssh-enum-users -p 22 scanme.nmap.org
   ```
   - The 'ssh-enum-users' script was unavailable; 'ssh-brute' was attempted but no output is included.

6. **Automated Vulnerability and CVE Script Sweeps**  
   ```
   nmap --script vuln -p 22 scanme.nmap.org
   nmap --script '*cve*' -p 22 scanme.nmap.org
   ```
   - Ran all tags or scripts flagged as vulnerabilities or referencing CVEs; no outputs were returned.

---

## Detailed Findings

### 1. SSH Service Identification
- **Result:** Port 22/tcp is open and running OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13.
- **Implication:** This is an outdated OpenSSH version; however, Nmap does not flag its version directly as vulnerable.

### 2. Protocol Version Support (ssHv1)
- **Result:** Only SSH protocol 2.0 is supported.
- **Implication:** No legacy/insecure SSHv1 supported. This is best practice.

### 3. Authentication Methods
- **Supported:**  
  - **publickey**
  - **password**
- **Security Consideration:** Enabling password authentication can increase risk if strong password policies, rate-limiting, or two-factor authentication are not enforced. No weak or legacy authentication methods (such as 'none' or 'keyboard-interactive') detected.

### 4. Supported SSH Algorithms  
(From `ssh2-enum-algos`; assessment for weak ciphers is included below.)

- **Key Exchange Algorithms (KEX):**
  - curve25519-sha256@libssh.org
  - ecdh-sha2-nistp256
  - ecdh-sha2-nistp384
  - ecdh-sha2-nistp521
  - diffie-hellman-group-exchange-sha256
  - **diffie-hellman-group-exchange-sha1 (legacy)**
  - **diffie-hellman-group14-sha1 (legacy)**
  - **diffie-hellman-group1-sha1 (weak/legacy, avoid)**

- **Host Key Algorithms:**
  - ssh-rsa
  - **ssh-dss (DSA, deprecated and weak; should be disabled)**
  - ecdsa-sha2-nistp256
  - ssh-ed25519

- **Encryption Algorithms:**
  - **arcfour/arcfour128/arcfour256 (weak, avoid)**
  - **aes*-cbc (aes128-cbc, aes192-cbc, aes256-cbc -- legacy mode, less secure than ctr/gcm)**
  - 3des-cbc, blowfish-cbc, cast128-cbc (legacy, weak or moderate security)
  - Modern: aes*-ctr, aes*-gcm@openssh.com, chacha20-poly1305@openssh.com

- **MAC Algorithms:**  
  Numerous including **hmac-md5**, **hmac-sha1**, and variants (considered weak by modern standards), along with stronger hmac-sha2-*, umac-*, etc.

- **Compression:**  
  - none
  - zlib@openssh.com

**Risk Note:**  
Several weak or deprecated algorithms are supported (notably diffie-hellman-group1-sha1, ssh-dss, arcfour, aes-*-cbc, hmac-md5, hmac-sha1). While their presence does not establish an exploit path, they represent increased risk if enabled and clients/server default to their use. Stronger cipher suite hardening is recommended.

### 5. Host Public Keys
- RSA (2048), DSA (1024), ECDSA (256), Ed25519 (256) key fingerprints captured for review/whitelisting if needed.

### 6. Vulnerability Scripts & CVE Checks
- **nmap --script vuln**  
  **Result:** No vulnerabilities or findings reported.
- **nmap --script '*cve*'**  
  **Result:** No applicable CVE checks or reported vulnerabilities for OpenSSH/SSH on the target.

**Key Limitation:**  
Nmap’s NSE script collection does **not** check for the majority of published OpenSSH vulnerabilities (e.g., CVE-2016-0777/0778, CVE-2015-5600, etc.), nor does it perform automated version-to-vulnerability mapping. Thus, many serious CVEs affecting OpenSSH 6.6.1p1 may remain undetected with Nmap alone.

---

## Summary Table of Findings

| Area          | Finding                                                                                              | Exploitable?                        | Nmap Detection?           |
|---------------|------------------------------------------------------------------------------------------------------|-------------------------------------|---------------------------|
| Port Status   | SSH (22/tcp) open                                                                                    | N/A                                 | Yes                       |
| Service       | OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (protocol 2.0 only)                                               | Outdated version, known CVEs exist* | Yes (no risk flagged)     |
| SSHv1         | Not supported                                                                                        | No                                  | Yes                       |
| Algorithms    | Legacy/weak ciphers, MACs, and hostkey algos supported; see above                                    | Theoretically, yes if negotiated    | Yes (listing only)        |
| Vulnerability | No active/exploitable vulnerabilities detected by Nmap scripts or CVE scan                            | No**                                | Yes (none flagged)        |
| Auth Methods  | publickey, password allowed                                                                          | Potential for brute force           | Yes                       |

> **\*** OpenSSH 6.6.1p1 is a legacy version, widely known to have vulnerabilities, but Nmap scripts do not actively check for most.
>  
> **\*\*** Absence of evidence is *not* evidence of absence—see “Limitations” below.

---

## Limitations

- **Nmap NSE scripts detect only vulnerabilities for which explicit script or matching logic exists**: Most OpenSSH CVEs are not covered by default or distributed scripts.
- **No automated "vulnerable version" mapping is present:** Identifying outdated or at-risk OpenSSH deployments requires additional tools or manual research.
- **No brute force/user enum performed:** User enumeration script not found; brute force script did not yield results.
- **Assessment only detects exposures visible to Nmap over the network:** Server side misconfigurations or vulnerabilities invisible to protocol parsing cannot be revealed.

---

## Recommendations

1. **Cryptographic Hardening**
   - Remove or disable legacy/weak algorithms (diffie-hellman-group1-sha1, ssh-dss, arcfour*, aes-*-cbc, 3des-cbc, hmac-md5, hmac-sha1, etc.).
   - Enforce use of strong ciphers and MACs (e.g., chacha20-poly1305, aes*-gcm, hmac-sha2).
   - Disable password authentication unless required; prefer public key authentication and consider additional protections (2FA, rate limiting, etc.).
2. **OpenSSH Version Upgrade**
   - The detected OpenSSH version (6.6.1p1) is many years old with numerous known vulnerabilities (see CVE databases). **Upgrade to a currently supported release** and monitor for ongoing patching needs.
3. **Further Assessment (Beyond Nmap)**
   - **Manually cross-reference the SSH version with online vulnerability databases (e.g., CVE, NVD, vendor advisories).**
   - **Consider running a dedicated vulnerability scanner or SSH audit tool** (e.g., Nessus, OpenVAS, ssh-audit) for a thorough evaluation of CVE impact and misconfiguration.
   - If required, request a follow-up assessment with more specialized or credentialed scanning tools.

---

## Conclusion

Based strictly on Nmap and its available scripts, **no exploitable SSH vulnerabilities or protocol weaknesses were detected on scanme.nmap.org (port 22)**. The SSH service does **not** offer the insecure SSHv1 protocol but does present several legacy ciphers and is running an outdated version of OpenSSH, which carries risk.

**IMPORTANT:**  
This report reflects only what Nmap’s current scripts can detect—not a guarantee of security or absence of vulnerabilities. The OpenSSH version in use is widely considered insecure and should be upgraded. For a definitive and comprehensive risk picture, further assessment is highly recommended.

---

*Prepared by: ReportWriter, Vulnerability Scan Report Specialist*  
*Reviewed and approved by: SeniorReviewer, Senior Penetration Tester*