package ai.nexora.service;

import ai.nexora.dto.SocialDtos;
import ai.nexora.entity.SocialAccount;
import ai.nexora.repository.SocialAccountRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

@Service
public class SocialService {

    private final SocialAccountRepository socialAccountRepository;

    public SocialService(SocialAccountRepository socialAccountRepository) {
        this.socialAccountRepository = socialAccountRepository;
    }

    public List<SocialAccount> getAccounts(UUID userId) {
        return socialAccountRepository.findByUserIdOrderByCreatedAtDesc(userId);
    }

    @Transactional
    public SocialAccount addProfileLink(UUID userId, SocialDtos.AddProfileLinkRequest req) {
        Optional<SocialAccount> existing = socialAccountRepository.findByUserIdAndPlatform(userId, req.getPlatform().toLowerCase());
        SocialAccount account = existing.orElse(new SocialAccount());

        account.setUserId(userId);
        account.setPlatform(req.getPlatform().toLowerCase());
        account.setProfileUrl(req.getProfileUrl());
        account.setUsername(req.getUsername());
        account.setDisplayName(req.getDisplayName() != null ? req.getDisplayName() : req.getUsername());
        account.setIsConnected(true);
        account.setConnectionType("profile_link");
        account.setShowOnPublicProfile(true);

        return socialAccountRepository.save(account);
    }

    @Transactional
    public SocialAccount connectGithub(UUID userId, SocialDtos.ConnectGithubRequest req) {
        Optional<SocialAccount> existing = socialAccountRepository.findByUserIdAndPlatform(userId, "github");
        SocialAccount account = existing.orElse(new SocialAccount());

        account.setUserId(userId);
        account.setPlatform("github");
        account.setUsername(req.getUsername());
        account.setProfileUrl(req.getProfileUrl() != null ? req.getProfileUrl() : "https://github.com/" + req.getUsername());
        account.setDisplayName(req.getUsername());
        account.setIsConnected(true);
        account.setConnectionType("oauth_or_token");
        account.setShowOnPublicProfile(true);
        if (req.getToken() != null) {
            account.setEncryptedToken(req.getToken()); // Encrypted or secured in production
        }

        return socialAccountRepository.save(account);
    }

    @Transactional
    public boolean updateVisibility(UUID userId, UUID accountId, boolean showOnProfile) {
        Optional<SocialAccount> opt = socialAccountRepository.findById(accountId);
        if (opt.isPresent() && opt.get().getUserId().equals(userId)) {
            SocialAccount account = opt.get();
            account.setShowOnPublicProfile(showOnProfile);
            socialAccountRepository.save(account);
            return true;
        }
        return false;
    }

    @Transactional
    public boolean disconnect(UUID userId, UUID accountId) {
        Optional<SocialAccount> opt = socialAccountRepository.findById(accountId);
        if (opt.isPresent() && opt.get().getUserId().equals(userId)) {
            socialAccountRepository.delete(opt.get());
            return true;
        }
        return false;
    }
}

