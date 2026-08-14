import pygame


def resolve_bullets(enemies, bullets):
    killed = []
    for bullet in bullets:
        hit = pygame.sprite.spritecollideany(bullet, enemies)
        if hit is not None and not getattr(hit, "dead", False):
            if hit.take_damage():
                killed.append(hit)
                hit.kill()
            bullet.kill()
    return killed


def resolve_player(enemies, player):
    return list(pygame.sprite.spritecollide(player, enemies, True))


def resolve_enemy_bullets(bullets, player):
    """Return True if any enemy bullet hit the player (removes the bullets)."""
    return len(pygame.sprite.spritecollide(player, bullets, True)) > 0